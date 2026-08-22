# ClubDash AI — Recommendation System Upgrade Plan

> **Scope:** Evolve the existing Q&A chatbot (`backend/app/assistant/`) into an intelligent,
> filter-aware recommendation system. Users can ask natural-language questions such as:
>
> *"I want to find a swimming pool that's chlorine-free and kid-friendly within 5 km."*
>
> The agent will parse intent, query the right data, and return a ranked, annotated list.

---

## Table of Contents

1. [Current State](#1-current-state)
2. [Target Architecture](#2-target-architecture)
3. [Phase 1 — Data Layer Enhancements](#3-phase-1--data-layer-enhancements)
4. [Phase 2 — Backend: New Recommendation Tools](#4-phase-2--backend-new-recommendation-tools)
5. [Phase 3 — Intent & Context Extraction](#5-phase-3--intent--context-extraction)
6. [Phase 4 — LLM Orchestration Upgrades](#6-phase-4--llm-orchestration-upgrades)
7. [Phase 5 — Frontend Enhancements](#7-phase-5--frontend-enhancements)
8. [Phase 6 — Security & Role Access](#8-phase-6--security--role-access)
9. [Phase 7 — Testing](#9-phase-7--testing)
10. [Rollout Sequence](#10-rollout-sequence)
11. [Open Questions](#11-open-questions)

---

## 1. Current State

| Component | File | What it does |
|---|---|---|
| Controller | `backend/app/assistant/controllers.py` | Single `/api/v1/assistant/chat` POST, JWT-gated, stores thread in Flask session |
| Service | `backend/app/assistant/services.py` | Calls LiteLLM with a fixed tool list per role; one round-trip + one follow-up |
| Tools | `backend/app/assistant/tools.py` | `ClubDashToolRegistry` — 8 read-only tools (bookings, events, availability, membership, club info, staff dashboard, staff bookings, staff attendance) |
| LLM | env `OPENAI_ASSISTANT_MODEL` (default `gpt-3.5-turbo`) | No streaming, no memory beyond current session |

**Limitations for recommendations:**
- Tools are tied to a single hard-coded `club_id = 1`.
- No awareness of facilities, amenities, or tags on courts/clubs.
- No geolocation — cannot answer "within 5 km".
- No ranking or scoring logic; responses are purely informational.
- No cross-club discovery — the system serves one club at a time.

---

## 2. Target Architecture

```
User Message
     │
     ▼
┌──────────────────────────────────┐
│  Intent Extractor (LLM call 1)   │  ← structured JSON: sport, amenities,
│  (new module: intent.py)         │    distance_km, date, time, budget, etc.
└──────────────────┬───────────────┘
                   │
                   ▼
┌──────────────────────────────────┐
│  Recommendation Engine           │
│  (new: recommendation_service.py)│  ← queries DB with filters + geo-sort
│   • find_facilities tool         │
│   • get_club_details tool        │
│   • get_available_slots tool     │
└──────────────────┬───────────────┘
                   │
                   ▼
┌──────────────────────────────────┐
│  Response Synthesiser (LLM call 2)│  ← formats a ranked, human-readable list
│  (existing AssistantService)     │    with distances, highlights, CTAs
└──────────────────┬───────────────┘
                   │
                   ▼
          Structured JSON response
          (list of recommendations
           + assistant narrative)
```

---

## 3. Phase 1 — Data Layer Enhancements

These schema changes unlock the filtering and geolocation capability the recommendation system needs.

### 3.1 Add Amenities & Tags to `Club` and `Court`

**File:** `backend/app/clubs/models.py`

```python
class Club(db.Model):
    # --- existing columns ---
    latitude   = db.Column(db.Float, nullable=True)   # e.g. 12.9716
    longitude  = db.Column(db.Float, nullable=True)   # e.g. 77.5946
    amenities  = db.Column(db.JSON, default=list)     # ["parking", "cafe", "locker"]
    tags       = db.Column(db.JSON, default=list)     # ["family-friendly", "women-only"]

class Court(db.Model):
    # --- existing columns ---
    amenities  = db.Column(db.JSON, default=list)     # ["chlorine-free", "heated", "indoor"]
    tags       = db.Column(db.JSON, default=list)     # ["kid-friendly", "accessible"]
    sport_type = db.Column(db.String(30), ...)        # already exists — keep
```

> **Why JSON columns?** Amenity lists grow over time without requiring schema migrations for every new tag. A JSON column is flexible and sufficient for filtering via `LIKE` / `JSON_CONTAINS` (MySQL/SQLite).

### 3.2 Database Migration

```bash
flask db migrate -m "add geolocation amenities tags to clubs courts"
flask db upgrade
```

Migration additions:
```python
op.add_column('clubs', sa.Column('latitude',  sa.Float()))
op.add_column('clubs', sa.Column('longitude', sa.Float()))
op.add_column('clubs', sa.Column('amenities', sa.JSON()))
op.add_column('clubs', sa.Column('tags',      sa.JSON()))
op.add_column('courts', sa.Column('amenities', sa.JSON()))
op.add_column('courts', sa.Column('tags',      sa.JSON()))
```

### 3.3 Admin API for Metadata

Add a lightweight admin endpoint so owners can set their club's geolocation and tags:

```
PATCH /api/v1/admin/clubs/<int:club_id>/metadata
Body: { "latitude": 12.97, "longitude": 77.59, "amenities": [...], "tags": [...] }
```

---

## 4. Phase 2 — Backend: New Recommendation Tools

### 4.1 New file: `backend/app/assistant/recommendation_service.py`

This module provides the core database-querying logic, independent of the LLM layer.

```python
import math
from app.clubs.models import Club, Court
from app.availability.services import AvailabilityService

def haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlon/2)**2)
    return R * 2 * math.asin(math.sqrt(a))

class RecommendationService:
    @staticmethod
    def find_clubs_by_criteria(criteria: dict) -> list[dict]:
        """
        criteria keys (all optional):
          sport_type   : str   e.g. "swimming"
          amenities    : list  e.g. ["chlorine-free"]
          tags         : list  e.g. ["kid-friendly"]
          user_lat     : float
          user_lon     : float
          distance_km  : float  e.g. 5.0
          max_fee      : float
          date         : str   YYYY-MM-DD (availability filter)
        Returns list of dicts sorted by distance (if geo provided) or name.
        """
        sport_type  = criteria.get("sport_type")
        amenities   = criteria.get("amenities", [])
        tags        = criteria.get("tags", [])
        user_lat    = criteria.get("user_lat")
        user_lon    = criteria.get("user_lon")
        distance_km = criteria.get("distance_km")
        date        = criteria.get("date")

        # Start with all courts joined to clubs
        query = Court.query.join(Club).filter(Court.is_active == True)

        if sport_type:
            query = query.filter(Court.sport_type.ilike(f"%{sport_type}%"))

        courts = query.all()
        results = []

        for court in courts:
            club = court.club

            # Amenity & tag filtering (JSON list containment)
            court_amenities = court.amenities or []
            court_tags      = court.tags or []
            club_amenities  = club.amenities or []
            club_tags       = club.tags or []
            all_amenities   = set(court_amenities + club_amenities)
            all_tags        = set(court_tags + club_tags)

            if amenities and not all(a in all_amenities for a in amenities):
                continue
            if tags and not all(t in all_tags for t in tags):
                continue

            # Geo filtering
            dist = None
            if user_lat and user_lon and club.latitude and club.longitude:
                dist = haversine_km(user_lat, user_lon, club.latitude, club.longitude)
                if distance_km and dist > distance_km:
                    continue

            results.append({
                "club_id":    club.id,
                "club_name":  club.name,
                "court_id":   court.id,
                "court_name": court.name,
                "sport_type": court.sport_type,
                "address":    club.address,
                "distance_km": round(dist, 2) if dist is not None else None,
                "amenities":  list(all_amenities),
                "tags":       list(all_tags),
                "open_time":  str(club.open_time),
                "close_time": str(club.close_time),
            })

        # Sort by distance if available, else alphabetically
        results.sort(key=lambda r: (r["distance_km"] or 9999, r["club_name"]))
        return results
```

### 4.2 New Tools in `backend/app/assistant/tools.py`

```python
@staticmethod
def find_facilities(sport_type=None, amenities=None, tags=None,
                    user_lat=None, user_lon=None, distance_km=None,
                    max_fee=None, date=None, **kwargs):
    """Search clubs/courts by criteria. Returns a ranked JSON list."""
    criteria = {k: v for k, v in {
        "sport_type": sport_type, "amenities": amenities, "tags": tags,
        "user_lat": user_lat, "user_lon": user_lon, "distance_km": distance_km,
        "date": date
    }.items() if v is not None}
    results = RecommendationService.find_clubs_by_criteria(criteria)
    return json.dumps(results)

@staticmethod
def get_club_details(club_id, **kwargs):
    """Full details for a specific club."""
    club = Club.query.get(club_id)
    if not club:
        return json.dumps({"error": "Club not found"})
    courts = Court.query.filter_by(club_id=club_id, is_active=True).all()
    return json.dumps({
        "club_id":    club.id,
        "name":       club.name,
        "address":    club.address,
        "open_time":  str(club.open_time),
        "close_time": str(club.close_time),
        "amenities":  club.amenities or [],
        "tags":       club.tags or [],
        "courts": [{"id": c.id, "name": c.name, "sport_type": c.sport_type,
                    "amenities": c.amenities or [], "tags": c.tags or []} for c in courts]
    })

@staticmethod
def get_available_slots_for_club(club_id, date=None, **kwargs):
    """Available slots for a specific club on a given date."""
    from datetime import date as today_date
    target = date or str(today_date.today())
    matrix = AvailabilityService.get_availability_matrix(club_id, target)
    if isinstance(matrix, tuple) and matrix[1]:
        return json.dumps(matrix[1])
    data = matrix[0] if isinstance(matrix, tuple) else matrix
    summary = {}
    for court in (data or {}).get("courts", []):
        available_slots = [s["time"] for s in court.get("slots", []) if s["status"] == "available"]
        summary[court["name"]] = available_slots
    return json.dumps({"date": target, "available_slots_by_court": summary})
```

### 4.3 Register New Tools in `services.py`

Add the following to `MEMBER_TOOLS` (available to all authenticated roles):

```python
{"type": "function", "function": {
    "name": "find_facilities",
    "description": (
        "Search for clubs or courts by sport type, amenities (e.g. chlorine-free, heated), "
        "tags (e.g. kid-friendly, women-only), distance from user location, date, and max fee. "
        "Returns a ranked list of matching facilities."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "sport_type":  {"type": "string",  "description": "e.g. swimming, tennis"},
            "amenities":   {"type": "array",   "items": {"type": "string"}},
            "tags":        {"type": "array",   "items": {"type": "string"}},
            "user_lat":    {"type": "number"},
            "user_lon":    {"type": "number"},
            "distance_km": {"type": "number"},
            "max_fee":     {"type": "number"},
            "date":        {"type": "string",  "description": "YYYY-MM-DD"}
        }
    }
}},
{"type": "function", "function": {
    "name": "get_club_details",
    "description": "Get full details of a specific club: amenities, courts, hours.",
    "parameters": {"type": "object", "properties": {
        "club_id": {"type": "integer"}
    }, "required": ["club_id"]}
}},
{"type": "function", "function": {
    "name": "get_available_slots_for_club",
    "description": "Get available booking slots for a club on a given date.",
    "parameters": {"type": "object", "properties": {
        "club_id": {"type": "integer"},
        "date":    {"type": "string", "description": "YYYY-MM-DD"}
    }, "required": ["club_id"]}
}},
```

---

## 5. Phase 3 — Intent & Context Extraction

### 5.1 New file: `backend/app/assistant/intent.py`

A dedicated pre-processing step that parses raw user messages into structured criteria
before passing them to the recommendation engine.

```python
import json
from litellm import completion

INTENT_SYSTEM_PROMPT = """
You are a sports facility search intent extractor.
Given a user message, extract search criteria as a JSON object.
Output ONLY valid JSON with these optional fields:
{
  "sport_type": "string or null",
  "amenities":  ["list of strings"] or [],
  "tags":       ["list of strings"] or [],
  "distance_km": number or null,
  "date":       "YYYY-MM-DD or null",
  "max_fee":    number or null,
  "is_recommendation_query": true/false
}

Examples:
- "swimming pool that's chlorine-free and kid-friendly within 5 km"
  → {"sport_type":"swimming","amenities":["chlorine-free"],"tags":["kid-friendly"],"distance_km":5,"is_recommendation_query":true}
- "What time does the club open?"
  → {"is_recommendation_query": false}
"""

def extract_intent(message: str, model: str) -> dict:
    resp = completion(
        model=model,
        messages=[
            {"role": "system", "content": INTENT_SYSTEM_PROMPT},
            {"role": "user",   "content": message}
        ],
        response_format={"type": "json_object"},
        temperature=0
    )
    try:
        return json.loads(resp.choices[0].message.content)
    except Exception:
        return {"is_recommendation_query": False}
```

### 5.2 User Location Passing

**Extended request body:**
```json
{
  "message": "Find a chlorine-free swimming pool within 5 km",
  "user_lat": 12.9716,
  "user_lon": 77.5946
}
```

**Controller update** (`controllers.py`):
```python
user_lat = data.get('user_lat')
user_lon = data.get('user_lon')
result, status = AssistantService.process_chat(user, message, thread_messages, user_lat, user_lon)
```

**Service update** — inject coordinates into tool args (only for tools that accept them):
```python
if func_name in ("find_facilities", "get_available_slots_for_club"):
    args["user_lat"] = user_lat
    args["user_lon"] = user_lon
```

> ⚠️ Also replace the hardcoded `club_id = 1` with a dynamic resolution. For `find_facilities`
> no club_id is needed; for single-club tools, resolve from the user's membership.

---

## 6. Phase 4 — LLM Orchestration Upgrades

### 6.1 Updated `AssistantService.process_chat()`

```python
@staticmethod
def process_chat(user, message, thread_messages=None, user_lat=None, user_lon=None):
    ...
    # Step 1: Extract intent
    intent = extract_intent(message, model)

    # Step 2: Augment system prompt with location hint for recommendation queries
    if intent.get("is_recommendation_query") and user_lat and user_lon:
        messages[0]["content"] += f"\nUser location: lat={user_lat}, lon={user_lon}."

    # Step 3: Multi-turn tool-call loop (up to 5 rounds)
    MAX_ROUNDS = 5
    final_text = None
    for _ in range(MAX_ROUNDS):
        response = completion(model=model, messages=messages,
                              tools=allowed_tools, tool_choice="auto")
        response_msg = response.choices[0].message
        messages.append(response_msg.model_dump())

        if not response_msg.tool_calls:
            final_text = response_msg.content
            break

        for tool_call in response_msg.tool_calls:
            # ... existing dispatch logic ...
            messages.append({...})
    ...
```

### 6.2 Updated System Prompts

**Member:**
```
You are a smart sports facility assistant for ClubDash.
You can answer questions AND make recommendations based on user preferences.
When a user asks to find a facility, use the `find_facilities` tool to search by sport type,
amenities (e.g. chlorine-free), tags (e.g. kid-friendly), distance, and date.
Present results as a numbered list with distance, highlights, and next available slot.
If no results match, explain why and suggest relaxing one filter.
```

**Response format for recommendations:**
```
1. **[Club Name]** — [X.X] km away
   🏊 Sport: [sport] | 📍 [address]
   ✅ Highlights: [amenities/tags that match the query]
   🕐 Next available: [slot or "see availability"]
```

---

## 7. Phase 5 — Frontend Enhancements

### 7.1 Location Permission & Payload

```javascript
// In the chat component
async function getUserLocation() {
  return new Promise((resolve) => {
    if (!navigator.geolocation) return resolve(null)
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
      () => resolve(null),
      { timeout: 5000 }
    )
  })
}

async function sendMessage(text) {
  const location = await getUserLocation()
  const payload = { message: text }
  if (location) {
    payload.user_lat = location.lat
    payload.user_lon = location.lon
  }
  const { data } = await api.post('/assistant/chat', payload)
  // render data.assistant_message + data.recommendations
}
```

### 7.2 New Component: `RecommendationCard.vue`

```vue
<template>
  <div class="glass p-4 rounded-lg space-y-1">
    <h3 class="font-semibold text-white">{{ item.club_name }}</h3>
    <p class="text-xs text-primary-400">
      {{ item.distance_km?.toFixed(1) }} km away
    </p>
    <p class="text-sm text-gray-400">{{ item.address }}</p>
    <div class="flex flex-wrap gap-1 mt-2">
      <span v-for="tag in item.tags" :key="tag"
            class="text-xs bg-white/10 rounded px-2 py-0.5 text-gray-300">
        {{ tag }}
      </span>
    </div>
    <div class="flex gap-2 mt-3">
      <button @click="$emit('book', item)"   class="btn-primary text-xs">Book a slot</button>
      <button @click="$emit('details', item)" class="btn-ghost  text-xs">Details →</button>
    </div>
  </div>
</template>
```

### 7.3 Follow-Up Action Chips

After recommendations render:
```
[ Book a slot ]  [ See events at this club ]  [ Get directions ]
```
- "Book a slot" → deep-links to `BookCourt.vue?club_id=<id>`
- "See events" → links to `Events.vue?club_id=<id>`
- "Get directions" → opens `maps.google.com?q=<address>`

### 7.4 Optional: Structured Response Envelope

Extend the API response to include a structured `recommendations` array alongside the narrative,
enabling card rendering without parsing the text:

```json
{
  "assistant_message": "Here are 3 pools near you...",
  "recommendations": [
    {
      "club_id": 2,
      "club_name": "AquaFit",
      "distance_km": 2.3,
      "sport_type": "swimming",
      "amenities": ["chlorine-free"],
      "tags": ["kid-friendly"],
      "address": "12 Lake View Rd"
    }
  ],
  "tools_used": ["find_facilities"],
  "response_id": "resp_abc123"
}
```

---

## 8. Phase 6 — Security & Role Access

| Role | Access | Notes |
|---|---|---|
| `player` (member) | `find_facilities`, `get_club_details`, `get_available_slots_for_club` + all existing member tools | Location data is ephemeral — never persisted |
| `front-desk` (staff) | All member tools + staff operational tools | May search on behalf of a walk-in visitor |
| `owner` | Currently blocked | Could enable in a future phase for multi-club benchmarking |
| Unauthenticated | ❌ Not allowed | All `/api/v1/assistant/*` endpoints remain JWT-protected |

**Privacy guardrails:**
- GPS coordinates are **never stored** to the database.
- Apply rate limiting: max 30 requests/minute per user (Flask-Limiter).
- Log tool calls (without PII) for analytics and abuse detection.

---

## 9. Phase 7 — Testing

### 9.1 Unit Tests (`tests/`)

| Test file | Coverage |
|---|---|
| `test_intent.py` | `extract_intent()` correctly maps NL to structured criteria |
| `test_recommendation_service.py` | Haversine distance, amenity filter, tag filter, sort order |
| `test_tools.py` | `find_facilities` returns correct JSON shape |

Sample:
```python
def test_haversine():
    dist = haversine_km(12.9716, 77.5946, 13.0168, 77.5946)
    assert 4.9 < dist < 5.1

def test_find_facilities_by_amenity(app_context, seed_clubs):
    results = RecommendationService.find_clubs_by_criteria({"amenities": ["chlorine-free"]})
    assert all("chlorine-free" in r["amenities"] for r in results)

def test_find_facilities_distance_filter(app_context, seed_clubs):
    results = RecommendationService.find_clubs_by_criteria({
        "user_lat": 12.9716, "user_lon": 77.5946, "distance_km": 3
    })
    assert all(r["distance_km"] <= 3 for r in results if r["distance_km"] is not None)
```

### 9.2 Integration Tests

```python
def test_recommendation_chat_roundtrip(client, auth_token):
    resp = client.post('/api/v1/assistant/chat',
        json={"message": "Find a chlorine-free pool within 5 km",
              "user_lat": 12.97, "user_lon": 77.59},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "find_facilities" in data["tools_used"]
    assert data["assistant_message"]
```

### 9.3 Manual QA Scenarios

| User query | Expected behaviour |
|---|---|
| "Find a chlorine-free swimming pool within 5 km" | `find_facilities` called; results filtered + sorted by distance |
| "Kid-friendly badminton court this Saturday?" | `find_facilities` + `get_available_slots_for_club` chained |
| "What time does the club open?" | Existing `get_club_information` used; no recommendation path |
| "Book me a court" | Bot clarifies it is read-only and offers to show available slots |
| Query with no matches | Bot explains why, suggests relaxing a filter |
| GPS denied by browser | Bot asks for neighbourhood/area as text fallback |

---

## 10. Rollout Sequence

| Week | Work |
|---|---|
| **1** | DB migrations (lat/lon, amenities, tags) · Admin PATCH metadata endpoint · Seed data |
| **2** | `RecommendationService` + Haversine · New tools (`find_facilities`, `get_club_details`, `get_available_slots_for_club`) · Unit tests |
| **3** | `intent.py` extractor · `AssistantService` multi-tool loop upgrade · Updated system prompts · Tool registration |
| **4** | Frontend: location permission · `RecommendationCard.vue` · Follow-up action chips · Integration tests |
| **5** | Rate limiting · Logging · Edge-case handling (no results, partial matches) · Latency review (target < 4 s) · Soft launch |

---

## 11. Open Questions

1. **Multi-club discovery:** Should members discover clubs they are not already members of?
   The hardcoded `club_id = 1` needs a policy decision before cross-club search ships.

2. **GPS denied fallback:** When `navigator.geolocation` is denied, should the bot ask the user
   to type their neighbourhood/area for a text-based proximity estimate?

3. **Amenity taxonomy:** Who owns the canonical tag vocabulary (e.g. `"chlorine-free"` vs
   `"salt-water"`)? An admin-managed controlled vocabulary prevents fragmentation across clubs.

4. **LLM cost:** Each recommendation query now uses 2–3 LLM calls. Consider caching
   intent extraction results for identical queries within the same session.

5. **Streaming:** Should the response stream progressively (SSE) for better perceived performance?

6. **Phase 2 booking CTA:** Should the assistant eventually *initiate* bookings, or remain read-only?
