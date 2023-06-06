import requests
with open('new-messages', 'r') as f:
  for line in f:
    print(line + ': ' + requests.get('http://127.0.0.1:9387/$' + str(line)).text)
    open('new-messages', 'w').close()