from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CG_API = os.environ.get("CG_API")
