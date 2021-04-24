import requests
import json

url = "http://192.168.100.137:3000/punches"

payload = json.dumps({
  "bag_id": "999",
  "score": "201",
  "count": "201"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

