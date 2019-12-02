import requests

url = "https://www.melon.com/search/keyword/index.json?jscallback=jQuery19108384283373015584_1575289329230&query=%25ED%2584%25B0&_=1575289329232"

response = requests.get(url).text

print(response)