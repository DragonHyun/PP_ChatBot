# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

musicName = 'despacito'
url = 'https://www.genie.co.kr/search/searchMain?query='
url = url + musicName
print(url)
request = requests.get(url)
html = request.text

soup = BeautifulSoup(html, 'html.parser')

musicName = soup.findAll('span', {'class':'t_point'})
#artists = soup.findAll('a', {'class':'artist ellipsis'})
#test = soup.findAll('td', {'class':'info'})

print(musicName)