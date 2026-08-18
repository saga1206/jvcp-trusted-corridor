import json
import os
from google import genai

client = genai.Client(api_key=os.environ.get("LLM_API_KEY"))

PLANNER_SYSTEM_PROMPT = """You are a Japan travel itinerary planner for Vietnamese travelers.
Given trip parameters, return ONLY valid JSON (no prose, no markdown fences) matching this shape:
{
  "days": [
    {
      "day_number": 1,
      "summary": "short string",
      "items": [
        {"time_of_day": "morning", "title": "string", "description": "string", "estimated_cost_jpy": 1500}
      ]
    }
  ]
}
Do not invent real-time prices as fact — use realistic round-number estimates and note in 'description' that costs are estimates.
Do not give legal, visa, or immigration advice."""

def generate_itinerary(destination, duration_days, budget_jpy, interests, travel_companions, preferred_language):
    user_prompt = f"""Destination: {destination}
Duration: {duration_days} days
Budget: {budget_jpy or 'not specified'} JPY
Interests: {interests or 'general'}
Travel companions: {travel_companions or 'not specified'}
Respond in {preferred_language} for text fields where natural, but keep JSON keys in English."""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_prompt,
        config={"system_instruction": PLANNER_SYSTEM_PROMPT},
    )
    text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(text)
