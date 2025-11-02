from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
from typing import Optional

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def promptPrint(
    starting_city: str,
    ending_city: str,
    number_of_people: int,
    age_group: str,
    trip_type: str,
    number_of_days: int,
    others: Optional[str] = None
):
    load_dotenv()
    api_key = os.getenv("api_key")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not found in .env file")

    genai.configure(api_key=api_key)
    client = genai.Client()

    prompt = f"""
    You are an expert travel AI specializing in personalized road trip itineraries.
    Your task is to generate a detailed {number_of_days}-day road trip itinerary from {starting_city} to {ending_city}.

    The itinerary must be tailored for the following context:
    - Group Size: {number_of_people} people
    - Age Group: {age_group}
    - Trip Theme: {trip_type}

    Please provide the response as a single, valid JSON object.
    Do NOT include markdown formatting, code fences, or explanations.

    The root of the JSON object must be a key named "itinerary" which contains an array of day objects.
    Each day object must have:
    - "day" (int)
    - "driving_summary": {"start", "end", "estimated_time"}
    - "activities": [{"name", "description"}]
    - "food_suggestions": [{"name", "description"}]
    - "overnight_lodging_suggestion": {"location", "description"}

    Also consider this user note:
    {others}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    text = response.text.strip()
    if text.startswith("```"):
        text = text.strip("`").replace("json", "").strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Model returned invalid JSON")

    return data


@app.get("/")
async def read_root():
    return {"message": "Travel Itinerary Generator is running."}


@app.get("/itinerary")
async def get_itinerary(
    starting_city: str,
    ending_city: str,
    number_of_people: int,
    age_group: str,
    trip_type: str,
    number_of_days: int,
    others: Optional[str] = None,
):
    data = promptPrint(
        starting_city=starting_city,
        ending_city=ending_city,
        number_of_people=number_of_people,
        age_group=age_group,
        trip_type=trip_type,
        number_of_days=number_of_days,
        others=others,
    )
    return data
