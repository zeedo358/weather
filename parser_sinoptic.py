import requests
from bs4 import BeautifulSoup
import configure
import re



def get_code(params = None):
	r = requests.get('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D1%82%D1%80%D1%83%D1%81%D0%BA%D0%B0%D0%B2%D0%B5%D1%86%D1%8C/2021-08-01',headers = configure.HEADERS, params = params)
	return r

def get_content_for_fallings(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('tr',class_ = None)[2].findAll('td')
	fallings = [item.text for item in items]
	return fallings

def get_content_for_temperature(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find('tr',class_ = 'temperature').findAll('td')
	temperature = [item.text for item in items]
	return temperature

def parsing():
	html = get_code()
	if html.status_code == 200:
		return kind_of_weather(html.text)
	else:
		return 1

print(parsing())