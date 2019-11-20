

import requests 


URL = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ILOMBARD38&format=1"

r = requests.get(url = URL)

#print(r.text)

#rowNumb = len(r.text.split('\n')) - 3
#print(rowNumb)
#row = r.text.split('\n')

#print(row)
print(r.text.split('\n')[len(r.text.split('\n')) - 3].split(',')[1])