import os
from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Environment variables not loaded, file .env not found")
else:
    load_dotenv()

PICKUP = os.getenv("PICKUP")
