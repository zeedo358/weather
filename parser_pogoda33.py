import requests
from bs4 import BeautifulSoup
import configure
import re



def get_code(params = None):
	r = requests.get('https://pogoda33.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%9A%D0%B8%D1%97%D0%B2/%D1%82%D0%B8%D0%B6%D0%B4%D0%B5%D0%BD%D1%8C',headers = configure.HEADERS, params = params)
	return r

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('h3',class_ = None)
	data = {item.text:[0]*7 for item in items[:-10:2]} # time starts with 00:00 step = 3 hours
	temperature  = [item.text for item in soup.find_all('span',class_ = 'forecast-temp')]
	kind_of_weather = [item.text for item in soup.find_all('div',class_ = 'col-3 col-md-2 sky-icon my-auto')]
	fallings = [item.text for item in soup.find_all('div',class_ = 'col-md-1 w-middle d-none d-md-block')[::2]]
	keys = [key for key in data.keys()]
	k = 0
	for i in range(0,7):
		for j in range(0,7):
			data[keys[i]][j] = [temperature[k],kind_of_weather[k],fallings[k]]
			k += 1
	return data
	
def parsing():
	html = get_code()
	if html.status_code == 200:
		return get_content(html.text)
	else:
		return 1

print(parsing())