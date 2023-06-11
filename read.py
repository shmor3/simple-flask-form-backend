import requests
with open('new-messages', 'r') as f:
  for line in f:
    print(line + ': ' + requests.get('https://forms.rstanford.com/$' + str(line)).text)
    open('new-messages', 'w').close()