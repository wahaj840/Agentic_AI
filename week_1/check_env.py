from dotenv import load_dotenv
import os
from pathlib import Path

# Always look for .env in the same folder as this script
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Fetch and print the API key
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("✅ OpenAI API Key Loaded Successfully!")
    print("Key starts with:", api_key[:15], "...")
else:
    print("❌ API key not found. Please check your .env file location and format.")
    print("Checked path:", env_path)