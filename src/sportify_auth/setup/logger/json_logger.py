import json
from datetime import datetime
from logging import StreamHandler, Formatter

import pytz


class JSONHandler(StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record) + self.terminator
            with self.lock:
                self.stream.write(msg)
                self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)


class JsonFormatter(Formatter):
    def converter(self, timestamp):
        tz = pytz.timezone("Europe/Moscow")
        dt = datetime.fromtimestamp(timestamp, tz)
        return dt

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            s = dt.isoformat()
        return s

    def format(self, record):
        log_record = {
            "asctime": self.formatTime(record),
            "levelname": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "request_id": record.request_id
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)
