# -*- coding:utf-8 -*-

import requests
import json

url = "https://www.melon.com/search/keyword/index.json"
params = {
    'jscallback': 'jQuery19108384283373015584_1575289329230',
    'query' : '터보',
} 

response = requests.get(url, params=params).text
json_string = response.replace(params['jscallback'] + '(', '').replace(');', '')
result_dict = json.loads(json_string)

print(result_dict)