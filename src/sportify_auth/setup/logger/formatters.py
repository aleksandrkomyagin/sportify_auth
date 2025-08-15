import logging
from datetime import datetime

import pytz


class DateTimeFormatter(logging.Formatter):
	def converter(self, timestamp):
		tz = pytz.timezone("Europe/Moscow")
		dt = datetime.fromtimestamp(timestamp, tz)
		return dt.timetuple()

	def formatTime(self, record, datefmt=None):
		ct = self.converter(record.created)
		if datefmt:
			s = datetime(*ct[:6]).strftime(datefmt)
		else:
			s = datetime(*ct[:6]).isoformat()
		return s
