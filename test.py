import requests

url = "https://api.kraken.com/0/public/Trades"

payload = {}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)