# -*- coding:utf-8 -*-

import requests
import requests
from bs4 import BeautifulSoup

musicName = '애상'
url = 'https://www.genie.co.kr/search/searchMain?query='
url = url + musicName

request = requests.get(url)

html = request.text

soup = BeautifulSoup(html, 'html.parser')

musicName = soup.findAll('span', {'class':'t_point'})
artists = soup.findAll('a', {'class':'artist ellipsis'})

print(artists)