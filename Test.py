# -*- coding: utf-8 -*-

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/keyboard')
def Keyboard():
    dataSend = {
        "type" : "buttons",
        "buttons" : ["버튼1", "도움말"]
    }
    return jsonify(dataSend)

@app.route('/message', methods = ['Post'])
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    if content == u"버튼1":
        dataSend = {
            "message": {
                "text" : "메뉴 목록!\n1. 메뉴1\n2. 메뉴2\n3. 메뉴3"
            }
        }
    elif content == u"도움말":
        dataSend = {
            "message" : {
                "text" : "도움말"
            }
        }
    elif u"메뉴1" in content:
        dataSend = {
            "message" : {
                "text" : "메뉴1의 텍스트"
            }
        }
    elif u"메뉴2" in content:
        dataSend = {
            "message" : {
                "text" : "메뉴2의 텍스트"
            }
        }
    else:
        dataSend = {
            "message" : {
                "text" : content
            }
        }
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)