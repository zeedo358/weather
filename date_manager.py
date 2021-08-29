from datetime import date

class DateManager:
	"""docstring for DataManager"""
	def __init__(self, usr_date):
		self.date_ = date(*map(int,usr_date.split('.')))
		self._days = ['понеділок','вівторок','середа','четвер','пʼятниця','субота','неділя']
		self._months = ['січня','лютого','березня','квітня','травня','червня','липня','серпня','вересня','жовтня','листопада','грудня']
	def get_day(self):
		#returns name of day of date was given
		return self._days[self.date_.weekday()]
	def get_month(self):
		#returns name of month of date was given
		return self._months[self.date_.month - 1]