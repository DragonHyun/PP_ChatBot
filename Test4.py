import requests
from bs4 import BeautifulSoup

request = requests.get('https://www.naver.com/')

html = request.text

soup = BeautifulSoup(html, 'html.parser')

words = soup.findAll('span', {'class':'ah_k'})