import requests
from bs4 import BeautifulSoup
import random


def get_images():
    cats = ['кот', 'кошка', 'котята']
    url = f'https://fonwall.ru/search?q={random.choice(cats)}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pictures = soup.find_all('img', class_='photo-item__img')
    clear_pictures = [item['src'] for item in pictures]
    return random.choice(clear_pictures)

