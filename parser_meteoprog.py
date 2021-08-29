import requests
from bs4 import BeautifulSoup
import configure
import re



def get_code(params = None):
	r = requests.get('https://www.meteoprog.ua/ua/weather/Kyiv/',headers = configure.HEADERS, params = params)
	r2 = requests.get('https://www.meteoprog.ua/ua/weather/Kyiv/6_10/',headers = configure.HEADERS, params = None)
	return r,r2

def kind_of_weather(html,html2):
	soup = BeautifulSoup(html, 'html.parser')
	soup2 = BeautifulSoup(html2, 'html.parser')
	kinds = [item.text for item in soup.find_all('div',class_ = 'infoPrognosis widthProg')] + [item.text for item in soup2.find_all('div',class_ = 'infoPrognosis widthProg')[:2]]
	names = [item.text for item in soup.find_all('span',class_ = 'bold')] + [item.text for item in soup2.find_all('span',class_ = 'bold')[:2]]
	temperature = [item.text for item in soup.find_all('span',class_ = 'temperature_value')[6:]] + [item.text for item in soup2.find_all('span',class_ = 'temperature_value')[6:15]]
	separator = r'\D\S+'
	desc = [''.join(re.findall(separator,item)[3:]) for item in kinds] + [''.join(re.findall(separator,item)[3:]) for item in kinds[-2:]]
	data = {names[i]:[desc[i]] for i in range(len(names))}
	i = 4
	for name in names:
		data[name]+= temperature[i-4:i]
		i+=4
	return data

def parsing():
	html,html2 = get_code()
	if html.status_code == 200:
		return kind_of_weather(html.text,html2.text)
	else:
		return 1

print(parsing())