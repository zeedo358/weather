import requests
from bs4 import BeautifulSoup
import configure
import re
from functools import reduce



def get_code(params = None):
	r = requests.get('https://www.google.com/search?q=погода+трускавець+03.08',headers = configure.HEADERS, params = params)
	return r
def get_content():
	data = {}

def get_content_for_fallings(html):
	soup = BeautifulSoup(html, 'html.parser')
	item = soup.find_all('div',class_ = 'XwOqJe')
	fallings = []
	for i,elem in enumerate(item):
		if i < 25:
			data = elem.get('aria-label')
			if 'вівторок' in data:
				fallings.append(data)
	#average fallings
	separator = r'\d+'
	avg = 0
	for elem in fallings:
		avg += int(re.search(separator,elem).group(0))
	avg /= len(fallings)
	#average for time:
	separator = r'\d+'
	for i,elem in enumerate(fallings):
		fallings[i] = int(re.search(separator,elem).group(0))
	fallings_for_time = [reduce(lambda x,y:x+y,fallings[0:7])/6,reduce(lambda x,y:x+y,fallings[7:13])/6,reduce(lambda x,y:x+y,fallings[13:19])/6,reduce(lambda x,y:x+y,fallings[19:24])/6]

	return fallings_for_time
#main temperature
def get_content_for_temperature(html):
	soup = BeautifulSoup(html, 'html.parser')
	item = soup.find('span',id = 'wob_tm').text
	return item
def kind_of_weather(html):
	soup = BeautifulSoup(html, 'html.parser')
	item = soup.find('span',id = 'wob_dc').text
	return item

def parsing():
	html = get_code()
	if html.status_code == 200:
		return get_content_for_fallings(html.text)
	else:
		return 1

print(parsing())