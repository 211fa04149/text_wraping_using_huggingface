from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

print(os.getenv("HF_API_TOKEN"))
