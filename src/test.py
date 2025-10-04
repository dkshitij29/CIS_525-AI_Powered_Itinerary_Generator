from google import genai
import os
from dotenv import load_dotenv
import google.generativeai
#from IPython.display import Markdown, display, update_display

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('api_key')

print("API Key Loaded:", os.getenv('api_key') is not None)

google.generativeai.configure()
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents = """"
            You are an expert travel planner.
            Generate a detailed 5-day road trip itinerary from Detroit, Michigan, to Houston, Texas.
            For each day, provide:
            1.  The main driving leg for the day (e.g., "Detroit, MI to Nashville, TN").
            2.  Estimated driving time.
            3.  Two interesting stops or activities along the way.
            4.  A suggestion for where to stay overnight.
        """
)
#response = gemini.generate_content(user_prompt)
print(response.text)
# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="Explain how AI works in a few words",
# )

# print(response.text)