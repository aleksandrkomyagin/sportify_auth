import logging

from sportify_auth.infrastructure.context.request_id import request_id_var


class RequestIdFilter(logging.Filter):
	def filter(self, record):
		record.request_id = request_id_var.get()
		return True
