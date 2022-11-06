import requests

url = 'https://crabeats.realtek.com/Food/AddMealRegister'
myobj = {'somekey': 'somevalue'}

x = requests.post(url, json = myobj)