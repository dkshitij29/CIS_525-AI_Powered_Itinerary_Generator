from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os, json
from typing import Optional
from google import genai
from google.genai import types

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000", # For React (default)
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

    client = genai.Client(api_key=api_key)


    prompt = f"""
        You are an expert travel AI specializing in personalized road trip itineraries.
        Your task is to generate a detailed {number_of_days}-day road trip itinerary from {starting_city} to {ending_city}.

        The itinerary must be tailored for the following context:
        - Group Size: {number_of_people} people
        - Age Group: {age_group}
        - Trip Theme: {trip_type}

        Please provide the response as a single, valid JSON object. Do not include any text, explanation, or markdown formatting outside of the JSON object itself.

        The root of the JSON object must be a key named "itinerary" which contains an array of day objects.

        Each day object in the array must conform to the following schema:
        - "day" (integer): The day number of the trip.
        - "driving_summary" (object): An object containing the driving details for the day.
        - "start" (string): The starting location for the day's drive.
        - "end" (string): The ending location for the day's drive.
        - "estimated_time" (string): The approximate driving duration.
        - "activities" (array of objects): An array of suggested activities. Each activity object must have:
        - "name" (string): The name of the place or activity.
        - "description" (string): A brief, one-sentence description explaining why it fits the trip theme.
        - "food_suggestions" (array of objects): An array of dining suggestions. Each food object must have:
        - "name" (string): The name of the restaurant or type of food.
        - "description" (string): A brief, one-sentence description (e.g., "Known for the best local BBQ").
        - "overnight_lodging_suggestion" (object): An object describing the lodging recommendation.
        - "location" (string): The city or area to stay in.
        - "description" (string): A brief suggestion for the type of lodging that fits the trip theme (e.g., "A boutique hotel in the downtown arts district.").
        
        And consider this special reuest.
        {others}
        """,


    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )

    text = response.text.strip()


    if text.startswith("```"):
        parts = text.split("```")
        if len(parts) >= 2:
            text = parts[1].replace("json", "", 1).strip()


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
