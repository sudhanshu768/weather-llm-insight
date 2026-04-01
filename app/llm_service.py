from google import genai
from app.config import GEMINI_API_KEY

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def explain_weather(user_query, data):
    """
    Generates a response using Gemini based ONLY on provided weather data.
    Ensures LLM does not hallucinate or ignore available data.
    """

    # Handle API error case (from backend)
    if "error" in data:
        return data["error"]

    # Extract values
    city = data.get("city")
    current_temp = data.get("current_temp")
    current_precip = data.get("current_precip")
    current_condition = data.get("current_condition")

    past_temp = data.get("past_temp")
    past_precip = data.get("past_precip")
    past_condition = data.get("past_condition")

    temp_diff = data.get("temp_diff")

    # Detect if query is about a specific past date
    is_past_query = (
        past_temp is not None
        and ("on" in user_query.lower() or "date" in user_query.lower())
    )

    # Build prompt (STRICT + CONTROLLED)
    prompt = f"""
You are a weather assistant.

IMPORTANT RULES:
- You MUST answer using ONLY the provided data.
- DO NOT say "I don't have enough information" if values are present.
- DO NOT hallucinate or add external knowledge.
- If past data exists, you MUST use it.
- If the question is about a specific date → answer ONLY using past data.

User Question:
{user_query}

Weather Data:

City: {city}

Current:
- Temperature: {current_temp}
- Rainfall: {current_precip}
- Condition: {current_condition}

Past:
- Temperature: {past_temp}
- Rainfall: {past_precip}
- Condition: {past_condition}

Temperature Change: {temp_diff}

Instructions:
- If past_temp is NOT None → use it in the answer
- If question includes a date → mention the date in answer
- Always include city name
- Always include unit °C
- Answer clearly in 1 sentence
Answer:
"""

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text