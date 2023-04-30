from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CG_API = os.environ.get("CG_API")


import requests
from bs4 import BeautifulSoup
from pprint import pprint


url = 'https://pikabu.ru/community/Cat'


response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
pictures = soup.find_all('img', class_='story-image__image')
# print(pictures)
clear_pictures = [item['data-src'] for item in pictures]
pprint(clear_pictures)



