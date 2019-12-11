import requests

r = requests.get(url = 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IMONZA49&format=1')
print(r.text)
extTemp = r.text.split('\n')[len(r.text.split('\n')) - 3].split(',')[1]
print(extTemp)