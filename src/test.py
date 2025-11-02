from google import genai
import os
from dotenv import load_dotenv
import google.generativeai
#from IPython.display import Markdown, display, update_display
from google.genai import types

def promptPrint():
    load_dotenv()
    os.environ['GOOGLE_API_KEY'] = os.getenv('api_key')

    print("API Key Loaded:", os.getenv('api_key') is not None)

    google.generativeai.configure()
    client = genai.Client()


    # 1. Define your input variables from the user request
    starting_city = "Detroit, MI"
    ending_city = "Houston, TX"
    number_of_people = 2
    age_group = "Young Adults (25-35)" # e.g., "Family with young children", "Seniors (65+)"
    trip_type = "Adventure and Food" # e.g., "Relaxing and Scenic", "Historical landmarks"
    number_of_days = 5
    others= "avoid bars"


    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
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
            """,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0))
            )

    print(response.text)
    return response.text

if __name__ == "__main__":
    promptPrint()