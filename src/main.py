from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import google.generativeai as genai
from google import genai
import os
from dotenv import load_dotenv
import google.generativeai
from typing import Optional

def promptPrint(
    starting_city: str,
    ending_city: str,
    number_of_people: int,
    age_group: str,
    trip_type: str,
    number_of_days: int,
    others:str 
):
    load_dotenv()
    os.environ['GOOGLE_API_KEY'] = os.getenv('api_key')

    print("API Key Loaded:", os.getenv('api_key') is not None)

    google.generativeai.configure()
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = f"""
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
            """
            )

    print(response.text)
    return response.text

app = FastAPI()

# --- API Endpoints ---

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
    others: Optional[str] = None 
):
    return promptPrint(
        starting_city=starting_city,
        ending_city=ending_city,
        number_of_people=number_of_people,
        age_group=age_group,
        trip_type=trip_type,
        number_of_days=number_of_days,
        others=others
    )

# import os
# import json
# from fastapi import FastAPI, HTTPException
# from dotenv import load_dotenv
# import google.generativeai as genai

# # --- 1. APPLICATION STARTUP LOGIC (runs only once) ---
# load_dotenv()
# API_KEY = os.getenv('GOOGLE_API_KEY')

# if not API_KEY:
#     raise ValueError("GOOGLE_API_KEY environment variable not set.")

# genai.configure(api_key=API_KEY)

# # Configure the model for reliable JSON output
# generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
# model = genai.GenerativeModel(
#     "gemini-1.5-flash",
#     generation_config=generation_config
# )

# app = FastAPI()

# # --- 2. API ENDPOINTS ---
# @app.get("/")
# async def read_root():
#     return {"message": "Travel Itinerary Generator is running."}

# @app.get("/itinerary")
# async def get_itinerary(
#     starting_city: str,
#     ending_city: str,
#     number_of_people: int,
#     age_group: str,
#     trip_type: str,
#     number_of_days: int,
#     others: str
# ):
#     prompt = f"""
#         You are an expert travel AI specializing in personalized road trip itineraries.
#         Your task is to generate a detailed {number_of_days}-day road trip itinerary from {starting_city} to {ending_city}.

#         The itinerary must be tailored for the following context:
#         - Group Size: {number_of_people} people
#         - Age Group: {age_group}
#         - Trip Theme: {trip_type}

#         Please provide the response as a single, valid JSON object. Do not include any text, explanation, or markdown formatting outside of the JSON object itself.

#         The root of the JSON object must be a key named "itinerary" which contains an array of day objects.

#         Each day object in the array must conform to the following schema:
#         - "day" (integer): The day number of the trip.
#         - "driving_summary" (object): An object containing the driving details for the day.
#         - "start" (string): The starting location for the day's drive.
#         - "end" (string): The ending location for the day's drive.
#         - "estimated_time" (string): The approximate driving duration.
#         - "activities" (array of objects): An array of suggested activities. Each activity object must have:
#         - "name" (string): The name of the place or activity.
#         - "description" (string): A brief, one-sentence description explaining why it fits the trip theme.
#         - "food_suggestions" (array of objects): An array of dining suggestions. Each food object must have:
#         - "name" (string): The name of the restaurant or type of food.
#         - "description" (string): A brief, one-sentence description (e.g., "Known for the best local BBQ").
#         - "overnight_lodging_suggestion" (object): An object describing the lodging recommendation.
#         - "location" (string): The city or area to stay in.
#         - "description" (string): A brief suggestion for the type of lodging that fits the trip theme (e.g., "A boutique hotel in the downtown arts district.").

#         Also, consider this special request: {others}.        
#         Provide the response as a single, valid JSON object with a root key "itinerary".
#         Ensure the schema for each day object is strictly followed.
#     """
    
#     try:
#         # Call the Google API
#         response = model.generate_content(prompt)
#         # Parse the JSON text into a Python dictionary and return it
#         return json.loads(response.text)
        
#     except Exception as e:
#         # If anything fails, catch the error and return a clean HTTP response
#         print(f"Error generating itinerary: {e}") # Log the error for debugging
#         raise HTTPException(
#             status_code=500,
#             detail="An internal error occurred while generating the itinerary."
#         )