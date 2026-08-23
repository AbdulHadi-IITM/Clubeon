import os
import json
import traceback
from flask import g
try:
    from mirascope import llm
except Exception:
    try:
        from mirascope.core import llm
    except Exception:
        llm = None

from app.config import Config
from app.assistant.tools import (
    get_my_bookings,
    get_events,
    get_availability,
    get_my_membership,
    get_club_information,
    get_staff_dashboard,
    get_staff_bookings,
    get_staff_attendance,
    get_court_status,
    find_facilities,
    get_club_details,
    get_available_slots_for_club,
    prepare_court_booking,
    confirm_court_booking,
    cancel_my_booking,
)

MEMBER_TOOLS = [
    get_my_bookings,
    get_events,
    get_availability,
    get_my_membership,
    get_club_information,
    find_facilities,
    get_club_details,
    get_available_slots_for_club,
    prepare_court_booking,
    confirm_court_booking,
    cancel_my_booking,
]

STAFF_TOOLS = MEMBER_TOOLS + [
    get_staff_dashboard,
    get_staff_bookings,
    get_staff_attendance,
    get_court_status,
]

from datetime import datetime, timedelta

SYSTEM_PROMPT_MEMBER = """You are an intelligent sports facility and concierge assistant for ClubDash.
Current Context: Today is {today_str}. Tomorrow is {tomorrow_str}. Current local time is {current_time}.

You can:
1. Answer questions about bookings, memberships, and events.
2. Recommend facilities and courts based on preferences (amenities like chlorine-free/heated/parking, sport, distance).
3. BOOK COURTS via a safe 2-step confirmation process:
   - Step 1 (Draft Hold): When a user asks to book or reserve a court (e.g. "Book Badminton Court 1 for tomorrow 6 PM"), call `prepare_court_booking`.
     * If the slot is available, present the court name, date, time slot, and notify them of the 5-minute hold. Ask them to confirm.
     * If `prepare_court_booking` returns 'status': 'unavailable', do NOT ask for confirmation. Inform the user that the requested slot is taken or passed, and list the available alternative slots returned in 'available_slots'.
   - Step 2 (Confirmation): When the user confirms (e.g. "Yes", "Confirm", "Go ahead", "Yes, please confirm and finalize this booking"), IMMEDIATELY call `confirm_court_booking(intent_id="")`. You do not need to ask for or know the intent_id; calling `confirm_court_booking(intent_id="")` automatically confirms their active hold. Provide the confirmed booking ID and receipt summary.
4. CANCEL bookings: When requested to cancel a booking, call `cancel_my_booking`.

Always format responses in structured, readable Markdown with bullet points, bold highlights, and clear next steps."""

SYSTEM_PROMPT_STAFF = """You are an assistant for ClubDash front-desk staff.
Current Context: Today is {today_str}. Tomorrow is {tomorrow_str}. Current local time is {current_time}.
You can view operational summaries, staff bookings, attendance, court status, search facility recommendations, and assist with booking reservations via `prepare_court_booking` and `confirm_court_booking`."""

class AssistantService:
    @staticmethod
    def process_chat(user, message, thread_messages=None, user_lat=None, user_lon=None):
        role = user.role
        
        # Store context in flask g for tools
        g.assistant_user_id = user.id
        g.assistant_club_id = 1
        g.assistant_user_lat = user_lat
        g.assistant_user_lon = user_lon

        now = datetime.now()
        today_str = now.strftime('%Y-%m-%d (%A)')
        tomorrow_str = (now + timedelta(days=1)).strftime('%Y-%m-%d (%A)')
        current_time = now.strftime('%H:%M')

        # Determine allowed tools based on role
        if role in ['front-desk', 'staff']:
            allowed_tools = STAFF_TOOLS
            system_prompt = SYSTEM_PROMPT_STAFF.format(today_str=today_str, tomorrow_str=tomorrow_str, current_time=current_time)
        else:
            allowed_tools = MEMBER_TOOLS
            system_prompt = SYSTEM_PROMPT_MEMBER.format(today_str=today_str, tomorrow_str=tomorrow_str, current_time=current_time)

        if thread_messages and len(thread_messages) > 0:
            messages = list(thread_messages)
            if messages[0].get("role") == "system":
                messages[0]["content"] = system_prompt
            else:
                messages.insert(0, {"role": "system", "content": system_prompt})
        else:
            messages = [{"role": "system", "content": system_prompt}]

        messages.append({"role": "user", "content": message})

        if llm is None:
            fallback_msg = "Hello! ClubDash AI Concierge is active. You can browse clubs, view schedules, and manage bookings from the menu."
            messages.append({"role": "assistant", "content": fallback_msg})
            return {
                "assistant_message": fallback_msg,
                "response_id": "resp_standby",
                "tools_used": [],
                "thread_messages": messages
            }, 200

        @llm.call(Config.ASSISTANT_MODEL, tools=allowed_tools)
        def run_agent(msgs: list):

            mirascope_msgs = []
            for m in msgs:
                r = m.get("role", "user")
                c = m.get("content", "")
                if r == "system":
                    mirascope_msgs.append(llm.messages.system(c))
                elif r == "assistant":
                    mirascope_msgs.append(llm.messages.assistant(c, model_id=None, provider_id=None))
                else:
                    mirascope_msgs.append(llm.messages.user(c))
            return mirascope_msgs

        try:
            response = run_agent(messages)
            tools_used = []

            while response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_name = getattr(tool_call, "name", None) or getattr(getattr(tool_call, "tool_type", None), "__name__", "tool")
                    tools_used.append(str(tool_name))
                response = response.resume(response.execute_tools())

            if hasattr(response, "content"):
                if isinstance(response.content, list):
                    final_text = "".join(getattr(part, "text", str(part)) for part in response.content)
                else:
                    final_text = str(response.content)
            elif hasattr(response, "text"):
                final_text = response.text() if callable(response.text) else str(response.text)
            else:
                final_text = str(response)

            messages.append({"role": "assistant", "content": final_text})

            return {
                "assistant_message": final_text,
                "response_id": f"resp_{abs(hash(final_text))}",
                "tools_used": tools_used,
                "thread_messages": messages
            }, 200
            
        except Exception as e:
            traceback.print_exc()
            return {"error": f"Internal AI error occurred: {str(e)}"}, 500

