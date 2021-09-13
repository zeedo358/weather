import asyncio
import time
import pickle

from make_urls import MakeUrls
from date_manager import DateManager
from info_parser import Parser


class Manager:
	"""Class which manages all information,making average data from all data was given"""
	def __init__(self,place,usr_date):
		self.place = place
		self.date_ = DateManager(usr_date)

	def _get_info(self):
		urls = MakeUrls(self.place,self.date_).make_urls()
		info_getter = Parser(urls,self.date_)
		info = asyncio.run(info_getter.get_info())
		return info

	def manage_info(self):
		data = self._get_info()
		managed_information = {'kind_of_weather':'','avg_temp':0,'avg_fallings':0,'temp':[0,0,0,0],'fallings':[0,0,0,0]}
		managed_information['kind_of_weather'] = data[0]['kind_of_weather'] # kind of weather from google website
		# managing data of avg fallings and avg temperature
		for info in data:
			managed_information['avg_temp'] += info['avg_temp']
			managed_information['avg_fallings'] += info['avg_fallings']
		else:
			managed_information['avg_temp'] = round(managed_information['avg_temp'] / len(data),1)
			managed_information['avg_fallings'] = round(managed_information['avg_fallings'] /len(data),1)

		# managing data of fallings and temperature for halfs of day
		len_temp = 0
		len_fallings = 0
		for i in range(len(managed_information['temp'])):
			for half_data_day in data:
				value_temp = half_data_day['temp'][i]
				value_falling = half_data_day['fallings'][i]
				if value_temp != None:
					managed_information['temp'][i] += value_temp
					len_temp += 1
				if value_falling != None:
					managed_information['fallings'][i] += value_falling
					len_fallings += 1
			else:
				managed_information['temp'][i] = round(managed_information['temp'][i] / len_temp,1)
				managed_information['fallings'][i] = round(managed_information['fallings'][i] / len_fallings,1)
				len_temp = 0
				len_fallings = 0

		return managed_information

def save_data(data):
	with open('data.pickle','wb') as file:
		pickle.dump(data,file)

def load_data():
	try:
		with open('data.pickle','rb') as file:
			return pickle.load(file)
	except FileNotFoundError:
		return {}



def main(city,date):
	data = load_data()
	last_time_updated = data.get(city) # 0 - last time of update, 1 - data
	if last_time_updated == None or last_time_updated.get(date) == None or time.time() - last_time_updated[date][0] > 1200:
		request = Manager(city,date)
		result_of_request = request.manage_info()
		if data:
			data[request.place].update({date:[time.time(),result_of_request]})
		else:
			data[request.place] = {date:[time.time(),result_of_request]}
		save_data(data)
	return data[city][date][1]



if __name__ == '__main__':
	t0 = time.time()
	print(main('трускавець','2021.09.14'))
	delta = time.time() - t0
	print(delta)
