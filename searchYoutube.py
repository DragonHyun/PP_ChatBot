# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import requests
import json

path = '/home/ubuntu/chromedriver'
driver = webdriver.Chrome(path)

musicName = '애상 10cm'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = 'https://www.youtube.com/results?search_query='
url = url + musicName

request = requests.get(url, headers = headers)
html = request.text

soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
videoID = soup.select('#body-content > ytd-video-renderer > div > vytd-thumbnail')

ID = videoID.find('a')['href']

print(ID)