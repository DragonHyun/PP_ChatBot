# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify, render_template
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from apiclient.discovery import build
from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import flask
import urllib
import requests
import json
import httplib2
import os
import os.path
import sys
import google.oauth2.credentials
import google_auth_oauthlib.flow


ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'

CLIENT_SECRETS_FILE = 'client_secrets.json'
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


app = Flask(__name__)

@app.route('/playMusic', methods = ['GET', 'POST'])
def playMusic():

    return render_template('playMusic.html')

@app.route('/searchPlaylist1', methods=['POST'])
def searchPlaylist1():

    playlistID = 'PLZqEXGV8c4fQlAprbGYiRCI7zAxLOVjGd'
    url = 'https://www.youtube.com/playlist?list='

    url = url + playlistID
    url = url + "a"
    url = url[:-1]
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all('tr', {'class':'pl-video yt-uix-tile'})
    playList1 = "♬오늘의 재생목록♬\n노래는 랜덤재생 됩니다 :)\n\n"
    playList2 = ""
    playList3 = ""
    playList4 = ""
    i = 1

    for title in titles:
        if i <= 70:
            playList1 = playList1 + str(i) + ". " + title['data-title'] + "\n"
        elif i <=140:
            playList2 = playList2 + str(i) + ". " + title['data-title'] + "\n"
        else:
            playList3 = playList3 + str(i) + ". " + title['data-title'] + "\n"
        i = i+1

    if playList1 == "":
        res = {
                "version" : "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "재생목록이 비어있어요!\n얼른 채워주세요~"
                                }
                        }
                    ],
                    "quickReplies": [
                        {
                            "label": "♬처음으로♬",
                            "action": "block",
                            "blockId": "5df21f7392690d0001fc0eee"
                        }
                    ]
                }
        }
    elif playList2 == "":
        res = {
                "version" : "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                            "text": playList1
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "label": "♬처음으로♬",
                            "action": "block",
                            "blockId": "5df21f7392690d0001fc0eee"
                        }
                    ]
                }
        }
    else:
        res = {
                "version" : "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                            "text": playList1
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "label": "♬다음 재생목록♬",
                            "action": "block",
                            "blockId": "5df8e845ffa74800014b4d7f",
                            "extra": {"playList2":playList2, "playList3":playList3}
                        },
                        {
                            "label": "♬처음으로♬",
                            "action": "block",
                            "blockId": "5df21f7392690d0001fc0eee"
                        }
                    ]
                }
        }

    return jsonify(res)

@app.route('/searchPlaylist2', methods=['POST'])
def searchPlaylist2():
    req = request.get_json()

    playList2 = req['action']['clientExtra']['playList2']
    playList3 = req['action']['clientExtra']['playList3']

    if playList3 == "":
        res = {
                "version" : "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": playList2
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "label": "♬이전 재생목록♬",
                            "action": "block",
                            "blockId": "5df4a4ae8192ac0001788b77",
                        },
                        {
                            "label": "♬처음으로♬",
                            "action": "block",
                            "blockId": "5df21f7392690d0001fc0eee"
                        }
                    ]
                }
        }
    else:
        res = {
                "version" : "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": playList2
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "label": "♬이전 재생목록♬",
                            "action": "block",
                            "blockId": "5df4a4ae8192ac0001788b77",
                        },
                        {
                            "label": "♬처음으로♬",
                            "action": "block",
                            "blockId": "5df21f7392690d0001fc0eee"
                        },
                        {
                            "label": "♬다음 재생목록♬",
                            "action": "block",
                            "blockId": "5df8e84f92690d0001fc2da2",
                            "extra": {"playList3":playList3}
                        }
                    ]
                }
        }
    return jsonify(res)


@app.route('/searchPlaylist3', methods=['POST'])
def searchPlaylist3():
    req = request.get_json()

    playList3 = req['action']['clientExtra']['playList3']

    res = {
            "version" : "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": playList3
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "label": "♬이전 재생목록♬",
                        "action": "block",
                        "blockId": "5df8e845ffa74800014b4d7f",
                    },
                    {
                        "label": "♬처음으로♬",
                        "action": "block",
                        "blockId": "5df21f7392690d0001fc0eee"
                    }
                ]
            }
    }
    return jsonify(res)

@app.route('/searchYoutube', methods=['POST'])
def searchYoutube():

    req = request.get_json()

    title = req['action']['clientExtra']['title']
    artist = req['action']['clientExtra']['artist']

    search = title + " " + artist
    url = 'https://www.youtube.com/results?search_query='
    url = url + search

    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html.parser')
    videoID = soup.find('a', {'class':'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})['href']
    videoTitle = soup.find('a', {'class':'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})['title']
    videoThumbnail = soup.find('div', {'class':'yt-thumb video-thumb'}).find('img', {'alt':''})['src']
    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": videoTitle,
                            "description": "제가 찾아온 노래에요~",
                            "thumbnail": {
                                "imageUrl": videoThumbnail
                            },
                            "buttons": [
                                {
                                    "action": "block",
                                    "label": "추가하기!",
                                    "blockId": "5df0791e92690d0001fbfe5b",
                                    "extra": {'videoID': videoID[9:]}
                                    #block insertMusic
                                    },
                                {
                                    "action": "block",
                                    "label": "원하는 노래가 아니야!",
                                    "blockID": "5dec89218192ac00017851de"
                                    #block wrongFind
                                }
                            ]
                        }
                    }
            ]
        }
    }
    return jsonify(res)


@app.route('/insertMusic', methods=['POST'])
def insertMusic():

    req = request.get_json()
    video_id = req["action"]["clientExtra"]["videoID"]

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    if os.path.isfile('credentials.json'):
        with open('credentials.json', 'r') as f:
            creds_data = json.load(f)
            creds = Credentials(creds_data['token'], refresh_token=creds_data['refresh_token'],token_uri=creds_data['token_uri'], client_id=creds_data['client_id'],client_secret= creds_data['client_secret'])
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, YOUTUBE_READ_WRITE_SCOPE)
        creds = flow.run_console()
        creds_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        print(creds_data)
        with open('credentials.json', 'w') as outfile:
            json.dump(creds_data, outfile)

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials = creds)

    youtube.playlistItems().insert(
            part='snippet',
            body=dict(
                snippet=dict(
                    playlistId = 'PLZqEXGV8c4fQlAprbGYiRCI7zAxLOVjGd',
                    resourceId=dict(
                        kind = 'youtube#video',
                        videoId = video_id)))).execute()

    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "재생목록에 추가되었습니다!"
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "label":"♬더 추가하기♬",
                        "action":"block",
                        "blockId":"5deb6e1dffa74800014b00ee"
                    },
                    {
                        "label":"♬처음으로♬",
                        "action":"block",
                        "blockId":"5df21f7392690d0001fc0eee"
                        #block homeComment
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
        if song == None:
            break
        if song.find('td', {'class':'none'}) is not None:
            break

        img = song.find('a',{'class':'cover'}).find('img')['src']
        title = song.find('td',{'class':'info'}).find('a',{'class':'title ellipsis'})
        artist = song.find('td',{'class':'info'}).find('a',{'class':'artist ellipsis'})


        title = title.get_text()
        if title[1:6] == "TITLE":
            title = title[6:]
        artist = artist.text

        imgList.append("http:" + img)
        titleList.append(title.strip())
        artistList.append(artist.strip())

        cnt = cnt + 1
        if cnt == 3:
            break

    if len(titleList) == 0:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "검색하신 노래를 못찾겠어요..\n제목과 가수를 입력하러 >가시겠어요?"
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "label": "♬자세히 검색♬",
                        "action": "block",
                        "blockId": "5deb6e1dffa74800014b00ee"
                        #block searchMusic
                    },
                    {
                        "label": "♬처음으로♬",
                        "action": "blcok",
                        "blockId": "5df21f7392690d0001fc0eee"
                        #block homeComment
                    }
                ]
            }
        }
    elif len(titleList) == 1:
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
                                            "blockID": "5dec8f6b92690d0001fbe3f4",
                                            "extra": {"title":titleList[0],
                                                "artist":artistList[0]}
                                        }
                                    ]
                                },
                                {
                                    "title": "찾는 노래가 없으신가요..?",
                                    "description": "자세히 제목과 가수를 입력해보시겠어요?",
                                    "tumbnail": {
                                        "imageUrl": {"https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80"
                                        }
                                    },
                                    "buttons": [
                                        {
                                            "action": "block",
                                            "label": "♬자세히 검색♬",
                                            "blockId": "5deb6e1dffa74800014b00ee"
                                        },
                                        {
                                            "action": "block",
                                            "label": "♬처음으로♬",
                                            "blockId": "5df21f7392690d0001fc0eee"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        }
    elif len(titleList) == 2:
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
                                    "title": "찾는 노래가 없으신가요..?",
                                    "description": "자세히 제목과 가수를 입력해보시겠어요?",
                                    "thumbnail":{
                                        "imageUrl": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80"
                                        },
                                    "buttons": [
                                        {
                                            "action": "block",
                                            "label": "♬자세히 검색♬",
                                            "blockId": "5deb6e1dffa74800014b00ee"
                                        },
                                        {
                                            "action": "block",
                                            "label": "♬처음으로♬",
                                            "blockId": "5df21f7392690d0001fc0eee"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        }
    else:
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
                                },
                                {
                                    "title": "찾는 노래가 없으신가요..?",
                                    "description": "자세히 제목과 가수를 입력해보시겠어요?",
                                    "thumbnail":{
                                        "imageUrl":"https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80"
                                    },
                                    "buttons": [
                                        {
                                            "action": "block",
                                            "label": "♬자세히 검색♬",
                                            "blockId": "5deb6e1dffa74800014b00ee"
                                        },
                                        {
                                            "action": "block",
                                            "label": "♬처음으로♬",
                                            "blockId": "5df21f7392690d0001fc0eee"
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

@app.route('/findBlock', methods=['POST'])
def findBlock():
    req = request.get_json()

    blockID = req["intent"]["id"]

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": blockID
                    }
                }
            ]
        }
    }

    return jsonify(res)

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host='0.0.0.0', port=5000, threaded=True)
