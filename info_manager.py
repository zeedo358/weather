from datetime import date
from make_urls import MakeUrls
from date_manager import DateManager
from parser import Parser

class Manager:
	"""Class which manages all information,making average data from all data was given"""
	def __init__(self,place,usr_date):
		self.place = place
		self.date_ = DateManager(usr_date)

	def _get_info(self):
		urls = MakeUrls(self.place,self.date_).make_url()
		info_getter = Parser(urls,self.date_)
		info = info_getter.get_info()
		return info

	def manage_info(self):
		day = str(self.date_.date_)
		data = self._get_info()
		managed_information = {day:{'kind_of_weather':'','avg_temp':0,'avg_fallings':0,'temp':[0,0,0,0],'fallings':[0,0,0,0]}}

		managed_information[day]['kind_of_weather'] = data[0][day]['kind_of_weather'] # kind of weather from google website
		# managing data of avg fallings and avg temperature
		for info in data:
			managed_information[day]['avg_temp'] += info[day]['avg_temp']
			managed_information[day]['avg_fallings'] += info[day]['avg_fallings']
		else:
			managed_information[day]['avg_temp'] = round(managed_information[day]['avg_temp'] / len(data),1)
			managed_information[day]['avg_fallings'] = round(managed_information[day]['avg_fallings'] /len(data),1)

		# managing data of fallings and temperature for halfs of day
		len_temp = 0
		len_fallings = 0
		for i in range(len(managed_information[day]['temp'])):
			for half_data_day in data:
				value_temp = half_data_day[day]['temp'][i]
				value_falling = half_data_day[day]['fallings'][i]
				if value_temp != None:
					managed_information[day]['temp'][i] += value_temp
					len_temp += 1
				if value_falling != None:
					managed_information[day]['fallings'][i] += value_falling
					len_fallings += 1
			else:
				managed_information[day]['temp'][i] = round(managed_information[day]['temp'][i] / len_temp,1)
				managed_information[day]['fallings'][i] = round(managed_information[day]['fallings'][i] / len_fallings,1)
				len_temp = 0
				len_fallings = 0

		return managed_information



print(Manager('трускавець','2021.09.14').manage_info())


