import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MAX_AGE_IN_SECONDS = int(os.getenv("MAX_AGE_IN_SECONDS", 60))
