from google import genai
from google.genai import types # New import
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from typing import List, Literal
import sys
from typing import get_args

# Load environment variables and set up the client
load_dotenv()
token = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=token)

# --- The Pydantic models remain the same ---
class Channel(BaseModel):
    name: str = Field(..., description="The name of the new Discord channel, formatted with aesthetic Unicode fonts.")
    type: Literal["text", "voice"] = Field(..., description="The type of the channel, either 'text' or 'voice'.")

class Category(BaseModel):
    name: str = Field(..., description="The name of the new Discord channel category, formatted with aesthetic Unicode fonts.")
    channels: List[Channel] = Field(..., description="A list of channels within this category.")

class ServerStructure(BaseModel):
    categories: List[Category] = Field(..., description="A list of categories for the server.")

# --- Define the system instruction for the model's behavior ---
system_instruction = """
You are a server setup bot for Discord. Your task is to generate a complete Discord server structure, including multiple categories and channels, based on a user-provided theme. The theme may be a single word or a simple sentence.

For all category and channel names, you must use aesthetic Unicode fonts.
The final output must be in JSON format and strictly follow the provided schema.
"""

# Get the theme from the user.
if len(sys.argv) < 2:
    print("Please provide a theme as a command-line argument.")
    sys.exit(1)

user_theme = sys.argv[1]

# Generate the content with the system instruction and user input
try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"Generate a server structure for the theme: {user_theme}",
        config=types.GenerateContentConfig( # Wrap the config in types.GenerateContentConfig
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=ServerStructure
        )
    )

    # Access the structured output
    server_structure = response.parsed

    # Print the proposed structure for your bot to use
    print(f"✨ Generated Server Structure for '{user_theme}' ✨")
    print("-" * 30)
    for category in server_structure.categories:
        print(f"Category: {category.name}")
        for channel in category.channels:
            print(f"  - Channel: {channel.name} ({channel.type})")
        print("-" * 30)

except Exception as e:
    print(f"An error occurred: {e}")