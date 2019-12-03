# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

musicName = 'despacito'
url = 'https://www.genie.co.kr/search/searchMain?query='
url = url + musicName

request = requests.get(url)
html = request.text

soup = BeautifulSoup(html, 'html.parser')
songs = soup.select('#body-content > div.search_song > div.search_result_detail > div.music-list-wrap > table > tbody > tr')

for song in songs:
    title = song.find('td',{'class':'info'}).find('a',{'class':'title ellipsis'})
    print(title.strip())
    
#musicName = soup.select('span', {'class':'t_point'})
#artists = soup.findAll('a', {'class':'artist ellipsis'})
#test = soup.findAll('td', {'class':'info'})