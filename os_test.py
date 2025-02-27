import os
from dotenv import load_dotenv

load_dotenv()
# token = os.environ.get("TELEGRAM_TOKEN")
# token = os.environ["TELEGRAM_TOKEN"]
token = os.getenv('TELEGRAM_TOKEN')
print(token)