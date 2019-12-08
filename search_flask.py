# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib
import requests
#import json

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'

app = Flask(__name__)

@app.route('/searchYoutube', methods=['POST'])
def test():
    req = request.get_json()
    ans = req['action']['clientExtra']['title'] + " " + req['action']['clientExtra']['artist']
    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": ans
                        }
                    }
            ]
        }
    }

    return jsonify(res)


@app.route('/searchMusic', methods=['POST'])
def searchMusic():
    
    imgList = []
    titleList = []
    artistList = []
    cnt = 0
    
    req = request.get_json()
    
    musicName = req["action"]["detailParams"]["sys_text"]["value"]
    #musicName = str(urllib.parse.quote(musicName))
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://www.genie.co.kr/search/searchMain?query='
    url = url + musicName

    req = requests.get(url, headers = headers)
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')
    songs = soup.select('#body-content > div.search_song > div.search_result_detail > div > table > tbody > tr')
    for song in songs:
        
        img = song.find('a',{'class':'cover'}).find('img')['src']
        
        title = song.find('td',{'class':'info'}).find('a',{'class':'title ellipsis'}).get_text()
        
        if title[1:6] == "TITLE":
            title = title[6:]
        
        artist = song.find('td',{'class':'info'}).find('a',{'class':'artist ellipsis'}).text
        
        imgList.append("http:" + img)
        titleList.append(title.strip())
        artistList.append(artist.strip())
        
        cnt = cnt + 1
        if cnt == 3:
            break
        
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": titleList[0],
                                "description": artistList[0],
                                "thumbnail": {
                                    "imageUrl": imgList[0]
                                },
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": "추가",
                                        "blockId": "5dec8f6b92690d0001fbe3f4",
                                        "extra": {'title': titleList[0], 'artist': artistList[0]}
                                    }
                                ]
                            },
                            {
                                "title": titleList[1],
                                "description": artistList[1],
                                "thumbnail": {
                                    "imageUrl": imgList[1]
                                },
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": "추가",
                                        "blockId": "5dec8f6b92690d0001fbe3f4",
                                        "extra": {'title': titleList[1], 'artist': artistList[1]}
                                    }
                                ]
                            },
                            {
                                "title": titleList[2],
                                "description": artistList[2],
                                "thumbnail": {
                                    "imageUrl": imgList[2]
                                },
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": "추가",
                                        "blockId": "5dec8f6b92690d0001fbe3f4",
                                        "extra": {'title': titleList[2], 'artist': artistList[2]}
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }
    return jsonify(res)


if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, threaded=True)