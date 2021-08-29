class MakeUrls():
	"""Class makes the url adress for making a request"""
	def __init__(self, place,date):
		self.place = place
		self.date = date
		self._transcription_leters = {'й':'i','ц':'ts','у':'u','к':'k','е':'e','н':'n','г':'h','ш':'sh','щ':'sch','з':'z','х':'kh','ї':'i','ф':'f','і':'i','в':'v','а':'a','п':'p','р':'r','о':'o','л':'l','д':'d','ж':'zh','є':'ie','ґ':'g','я':'ia','ч':'ch','с':'s','м':'m','и':'y','т':'t','ь':'','б':'b','ю':'iu'}
	
	def make_url(self):
		google_url = 'https://www.google.com/search?q=погода+{}+{}.{}'.format(self.place,self.date.date_.strftime("%d"),self.date.date_.strftime("%m"))
		sinoptik_url = 'https://ua.sinoptik.ua/погода-{}/{}'.format(self.place,str(self.date.date_))
		pogoda33_url = 'https://pogoda33.ua/погода-{}/тиждень'.format(self.place)
		meteoprog_url = ['https://www.meteoprog.ua/ua/weather/{}/'.format(self._localize_place()),'https://www.meteoprog.ua/ua/weather/{}/6_10/'.format(self._localize_place())]
		meteotrend_url = 'https://ua.meteotrend.com/forecast/ua/{}/'.format(self._localize_place())
		return {'google':google_url,'sinoptik':sinoptik_url,'pogoda33':pogoda33_url,'meteoprog':meteoprog_url,'meteotrend':meteotrend_url}

	def _localize_place(self):
		localized_place = self.place
		for key,value in self._transcription_leters.items():
			localized_place = localized_place.replace(key,value)
		return localized_place


