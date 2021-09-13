import asyncio
import re
import datetime

import aiohttp
from bs4 import BeautifulSoup

import configure

class Parser:
	"""Main class of parsers, which includes 2 functions for getting html code of urls"""
	def __init__(self,urls,date):
		self.urls = dict(urls)
		self.date = date
		self.registered_methods = []

	async def _make_request(self,url):
		# making a request to a web site
		async with aiohttp.ClientSession() as session:
			async with session.get(url,headers = configure.HEADERS) as response:
				if response.status == 200:
					return await response.text()
				else:
					return 

	async def _get_soup(self,url):
		# returns BeatutifulSoup object for working with it
		result = await self._make_request(url)
		return BeautifulSoup(result,'html.parser')

	async def get_info(self):
		#calling all parsers
		info = await asyncio.gather(self.google_parser(),
		self.meteotrend_parser(),
		self.meteoprog_parser(),
		self.pogoda33_parser(),
		self.sinoptik_parser())

		return info

	async def google_parser(self):
		# taking information from the google website
		day = str(self.date.date_)
		separator = r'\d+'
		information = {day:{'kind_of_weather':'','avg_temp':0,'avg_fallings':0,'temp':[None,None,None,None],'fallings':[None,None,None,None]}}
		#get fallings
		soup = await self._get_soup(self.urls['google'])
		items = soup.find_all('div',class_ = 'XwOqJe')
		fallings = []
		for i,elem in enumerate(items):
			# taking 24 hours for day we need
			if i < (24 - datetime.datetime.now().hour) + ((self.date.date_ - self.date.date_.today()).days * 24) and i >= (23 - datetime.datetime.now().hour) + (((self.date.date_ - self.date.date_.today()).days -1) * 24): # 24 hours
				data = elem.get('aria-label')
				if self.date.get_day() in data:
					fallings.append(int(re.search(separator,data).group(0)))

		#average fallings for time:
		if self.date.date_ != self.date.date_.today():
			fallings_for_time = [sum(fallings[0:7])/6,sum(fallings[7:13])/6,sum(fallings[13:19])/6,sum(fallings[19:24])/6] # 6 hour half of day
			information[day]['fallings'] = fallings_for_time

		# average fallings
		avg = sum(fallings) / len(fallings)
		information[day]['avg_fallings'] = avg

		#average temperature
		temperature = soup.find('span',id = 'wob_tm').text
		information[day]['avg_temp'] = float(temperature)

		#kind of weather
		kind = soup.find('span',id = 'wob_dc').text
		information[day]['kind_of_weather'] = kind

		return information

	async def meteotrend_parser(self):
		# taking information from the meteotrend website
		day = str(self.date.date_)
		information = {day:{'kind_of_weather':'','avg_temp':0,'avg_fallings':0,'temp':[None,None,None,None],'fallings':[None,None,None,None]}}
		separator = r'\d+\,\d+'
		times = ['ніч','ранок','день','вечір']
		fell_rain = 0
		searched_day = '{}, {} {} {}'.format(self.date.get_day(),self.date.date_.day,self.date.get_month(),self.date.date_.year)


		soup = await self._get_soup(self.urls['meteotrend'])
		blocks = soup.find_all('div',class_ = 'box')

		for block in blocks:
			name = block.find('h5').text
			# checking is this day we're searching
			if repr(name.replace('\'','ʼ')) == repr(searched_day):
				continue
			info_for_blocks = block.findAll('div',class_ = 'm7')
			for info in info_for_blocks:
				key = times.index(info.find('td',class_='dtm').find('b').text)
				fallings = [item.text for item in info.find('div',class_ = 'wtpo').find_all('b') if 'мм' in item.text and len(item.text) <= 6]
				# converting fell rain into percents of fallings
				if fallings:
					fell_rain = float(fallings[0][:-2].replace(',','.')) * 30
					if fell_rain > 100: fell_rain = 100
					information[day]['fallings'][key] = fell_rain
				else:
					information[day]['fallings'][key] = 0

				data = [item.text for item in info.find('td',class_ = 't0').find_all('b')]
				if len(data) == 3:
					avg_temp = (float(data[0])+float(data[1][:3]))/2
					mini_desc = data[2]
				else:
					avg_temp = (float(data[0][:3])+float(data[0][:3]))/2
					mini_desc = data[1]
				information[day]['temp'][key] = avg_temp
				#taking kind of weather from middle time of day 
				if key == 2:
					information[day]['kind_of_weather'] = mini_desc
		# average temperature, fallings
		len_temp = 0
		len_fallings = 0
		for elem,elem2 in zip(information[day]['temp'],information[day]['fallings']):
			if elem != None:
				information[day]['avg_temp'] += elem
				len_temp += 1
			if elem2 != None:
				information[day]['avg_fallings'] += elem2
				len_fallings += 1

		information[day]['avg_temp'] /= len_temp
		information[day]['avg_fallings'] /= len_fallings

		return information

	async def meteoprog_parser(self):
		# taking information from the meteoprog website
		day = str(self.date.date_)
		information = {day:{'kind_of_weather':'','avg_temp':0,'avg_fallings':0,'temp':[None,None,None,None],'fallings':[None,None,None,None]}}
		searched_day = '{} {},'.format(self.date.date_.day,self.date.get_month())
	
		soup,soup2 = await asyncio.gather(*[self._get_soup(url) for url in self.urls['meteoprog']])

		# getting kinds of weather for days of week
		kinds = [item.text for item in soup.find_all('div',class_ = 'infoPrognosis widthProg')] + [item.text for item in soup2.find_all('div',class_ = 'infoPrognosis widthProg')[:2]]
		# getting all names of days
		names = [item.text for item in soup.find_all('span',class_ = 'bold')] + [item.text for item in soup2.find_all('span',class_ = 'bold')[:2]]
		# getting all info of temperature of all days at week
		temperature = [item.text for item in soup.find_all('span',class_ = 'temperature_value')[6:]] + [item.text for item in soup2.find_all('span',class_ = 'temperature_value')[6:15]]
		separator = r'\D\S+'
		# getting desctiption of weather
		desc = [''.join(re.findall(separator,item)[3:]) for item in kinds] + [''.join(re.findall(separator,item)[3:]) for item in kinds[-2:]]
		data = {names[i]:[desc[i]] for i in range(len(names))}

		i = 4
		for name in names:
			data[name]+= temperature[i-4:i]
			i += 4
			
		#kind of weather
		information[day]['kind_of_weather'] = data[searched_day][0].split('.')[0]
		# avg temp and temperature
		len_temp = 0
		for i,elem in enumerate(data[searched_day][1:]):
			information[day]['temp'][i] = float(elem)
			if elem != None:
				information[day]['avg_temp'] += float(elem)
				len_temp += 1
		information[day]['avg_temp'] /= len_temp

		return information

	async def pogoda33_parser(self):
		# taking information from the pogoda33 website
		day = str(self.date.date_)
		information = {day:{'kind_of_weather':'','avg_temp':0,'avg_fallings':0,'temp':[None,None,None,None],'fallings':[None,None,None,None]}}

		soup = await self._get_soup(self.urls['pogoda33'])
		# time starts with 00:00 step = 3 hours
		# parsing all information for all days in week
		temperature  = [item.text for item in soup.find_all('span',class_ = 'forecast-temp')]
		kind_of_weather = [item.text for item in soup.find_all('div',class_ = 'col-3 col-md-2 sky-icon my-auto')]
		fallings = [item.text for item in soup.find_all('div',class_ = 'col-md-1 w-middle d-none d-md-block')[::2]]

		division_in_days = ((self.date.date_ - self.date.date_.today()).days) * 8 # 8 hours at half a day
		# temp and avg_temp
		information[day]['temp'] = [sum(float(elem[:-1]) for elem in temperature[division_in_days:division_in_days + 3])/3,sum(float(elem[:-1]) for elem in temperature[division_in_days+3:division_in_days + 5])/2,sum(float(elem[:-1]) for elem in temperature[division_in_days+5:division_in_days + 7])/2,sum(float(elem[:-1]) for elem in temperature[division_in_days+7:division_in_days + 8])]
		information[day]['avg_temp'] = sum(information[day]['temp']) / len(information[day]['temp'])
		#kind of weather
		information[day]['kind_of_weather'] = kind_of_weather[int((division_in_days * 2 + 9) / 2)]
		# converting fallings into percents
		for i,elem in enumerate(fallings):
			fallings[i] = float(elem[:-2].replace(',','.').replace(' ','')) * 30
			if fallings[i] > 100: fallings[i] = 100
		#falling and avg_fallings
		information[day]['fallings'] = [float(sum(fallings[division_in_days:division_in_days + 3])/3),float(sum(fallings[division_in_days+3:division_in_days + 5])/2),float(sum(fallings[division_in_days+5:division_in_days + 7])/2),float(sum(fallings[division_in_days+7:division_in_days + 8]))]
		information[day]['avg_fallings'] = sum(information[day]['fallings']) / len(information[day]['fallings'])

		return information

	async def sinoptik_parser(self):
		# taking information from the sinoptik website
		day = str(self.date.date_)
		information = {day:{'kind_of_weather':'','avg_temp':0,'avg_fallings':0,'temp':[0,0,0,0],'fallings':[0,0,0,0]}}
		#getting all information for the day
		soup = await self._get_soup(self.urls['sinoptik'])
		items = soup.find_all('tr',class_ = None)[2].findAll('td')
		fallings = [item.text for item in items]
		items = soup.find('tr',class_ = 'temperature').findAll('td')
		temperature = [item.text for item in items]

		#fallings and temperature
		i = 0
		for j in range(len(fallings)):
			if j % 2 == 0 and j != 0:
				information[day]['fallings'][i] /= 2
				information[day]['temp'][i] /= 2
				i+=1
			if fallings[j] == '-':
				information[day]['fallings'][i] += 0
			else:
				information[day]['fallings'][i] += float(fallings[j])
			information[day]['temp'][i] += float(temperature[j][:-1])
		else:
			information[day]['fallings'][-1] /= 2
			information[day]['temp'][-1] /= 2

		#avg_fallings and avg_temp
		information[day]['avg_fallings'] = sum(information[day]['fallings'])/len(information[day]['fallings'])
		information[day]['avg_temp'] = sum(information[day]['temp'])/len(information[day]['temp'])
		
		return information

		
if __name__ == '__main__':
	from make_urls import MakeUrls
	from date_manager import DateManager
	date_ = DateManager('2021.09.14')
	urls = MakeUrls('трускавець',date_).make_url()
	info_getter = Parser(urls,date_)
	info = asyncio.run(info_getter.get_info())
	print(info)