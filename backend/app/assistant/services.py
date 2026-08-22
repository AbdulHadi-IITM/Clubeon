import os
import json
import traceback
from flask import g
from mirascope import llm
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
]

STAFF_TOOLS = MEMBER_TOOLS + [
    get_staff_dashboard,
    get_staff_bookings,
    get_staff_attendance,
    get_court_status,
]

SYSTEM_PROMPT_MEMBER = """You are an intelligent sports facility and club assistant for ClubDash.
You can answer questions about bookings, memberships, and events, AND provide smart recommendations based on user preferences.
When a user asks to find facilities, courts, or pools (e.g. chlorine-free, kid-friendly, heated, indoor, parking, distance, sport type), use the `find_facilities` tool.
If specific available slots are requested for a club, use `get_available_slots_for_club`.

Format recommendations in structured Markdown:
- Numbered facility name and distance (e.g. "1. **[Club Name]** — [X.X] km away")
- Sport type, address, and operating hours
- Matching highlights (amenities & tags)
- Available time slots if requested

If no facilities match all criteria, explain why and suggest relaxing one filter.
You are read-only and cannot perform direct booking transactions."""

SYSTEM_PROMPT_STAFF = """You are a helpful assistant for ClubDash front-desk staff.
You can access operational summaries, staff bookings, attendance, court status, and search facility recommendations."""

class AssistantService:
    @staticmethod
    def process_chat(user, message, thread_messages=None, user_lat=None, user_lon=None):
        role = user.role
        
        # Store context in flask g for tools
        g.assistant_user_id = user.id
        g.assistant_club_id = 1
        g.assistant_user_lat = user_lat
        g.assistant_user_lon = user_lon

        # Determine allowed tools based on role
        if role == 'player':
            allowed_tools = MEMBER_TOOLS
            system_prompt = SYSTEM_PROMPT_MEMBER
        elif role == 'front-desk':
            allowed_tools = STAFF_TOOLS
            system_prompt = SYSTEM_PROMPT_STAFF
        else:
            return {"error": "Role not permitted"}, 403

        messages = thread_messages or [{"role": "system", "content": system_prompt}]
        messages.append({"role": "user", "content": message})
        
        # Determine model and provider:
        provider = os.environ.get("MODEL_PROVIDER", "").strip().lower()
        raw_model = os.environ.get("ASSISTANT_MODEL") or os.environ.get("OPENAI_ASSISTANT_MODEL", "gemini-2.0-flash").strip()

        if provider:
            model_name = raw_model.split("/", 1)[1] if "/" in raw_model else raw_model
            model = f"{provider}/{model_name}"
        elif "/" in raw_model:
            model = raw_model
        elif raw_model.startswith("gemini"):
            model = f"google/{raw_model}"
        elif raw_model.startswith("claude"):
            model = f"anthropic/{raw_model}"
        else:
            model = f"openai/{raw_model}"

        # Ensure Google API key fallback if using google/gemini models
        if (model.startswith("google/") or model.startswith("gemini")) and not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
            key = os.environ.get("OPENAI_API_KEY", "")
            if key.startswith("AIzaSy"):
                os.environ["GEMINI_API_KEY"] = key
                os.environ["GOOGLE_API_KEY"] = key

        @llm.call(model, tools=allowed_tools)
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

