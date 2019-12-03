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

for i in range(len(musicName)):
    musicName = musicName[i].text.strip().split('\n')[0]
    artists = artists[i].text.strip().split('\n')[0]
    print('{0:3d}. {1} - {2}'.format(i + 1, musicName, artists))