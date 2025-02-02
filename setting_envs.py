import os
import sys
from dotenv import load_dotenv

#setting up env path 
env_path = r"D:\common_credentials\.env"

#load env variables
load_dotenv(dotenv_path=env_path)

## storing into the py variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#store the variable to env
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY