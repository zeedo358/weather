import requests
from bs4 import BeautifulSoup
import configure
import re



def get_code(params = None):
	r = requests.get('https://ua.meteotrend.com/forecast/ua/truskavets/',headers = configure.HEADERS, params = params)
	return r

def kind_of_weather(html):
	soup = BeautifulSoup(html, 'html.parser')
	blocks = soup.find_all('div',class_ = 'box')
	data = {}
	all_data = {}
	for block in blocks:
		info_for_blocks = block.findAll('div',class_ = 'm7')
		name = block.find('h5').text
		for info in info_for_blocks:
			key = info.find('td',class_='dtm').find('b').text
			data[key] = [item.text for item in info.find('td',class_ = 't0').find_all('b')] +[item.text for item in info.find('div',class_ = 'wtpo').find_all('b') if 'мм' in item.text and len(item.text) <= 6]
		all_data[name] = dict(data)

	return all_data

def parsing():
	html = get_code()
	if html.status_code == 200:
		return kind_of_weather(html.text)
	else:
		return 1

print(parsing())