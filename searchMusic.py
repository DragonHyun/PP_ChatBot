# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

musicName = 'despacito'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = 'https://www.genie.co.kr/search/searchMain?query='
url = url + musicName

request = requests.get(url, headers = headers)
html = request.text

soup = BeautifulSoup(html, 'html.parser')
songs = soup.select('#body-content > div.search_song > div.search_result_detail > div > table > tbody > tr')

for song in songs:
    title = song.find('td',{'class':'info'}).find('a',{'class':'title ellipsis'}).find('span',{'class':'t_point'})
    if title == None:
        title = song.find('td',{'class':'info'}).find('a',{'class':'title ellipsis'}).find('span',{'class':'icon icon-title'}).text
    else:
        title = title.text
    
    artists = song.find('td',{'class':'info'}).find('a', {'class':'artist ellipsis'}).text
    print(title + " - " + artists.strip())