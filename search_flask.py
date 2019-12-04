# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'

app = Flask(__name__)

@app.route('/searchMusic', methods=['POST'])
def searchMusic():
    
    req = request.get_json()
    
    musicName = req["action"]["detailParams"]["sys_music_name"]["value"]
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://www.genie.co.kr/search/searchMain?query='
    url = url + musicName

    request = requests.get(url, headers = headers)
    html = request.text

    soup = BeautifulSoup(html, 'html.parser')
    songs = soup.select('#body-content > div.search_song > div.search_result_detail > div > table > tbody > tr')
    for song in songs:
        title = song.find('td',{'class':'info'}).find('a',{'class':'title ellipsis'}).get_text()
        
        if title[1:6] == "TITLE":
            title = title[6:]
        
        artists = song.find('td',{'class':'info'}).find('a',{'class':'artist ellipsis'}).text
    
    answer = title.strip() + " - " + artists.strip()
    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }

    return jsonify(res)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, threaded=True)