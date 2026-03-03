import logging
import json
import datetime as dt
from typing import Optional

LOG_RECORD_ATTRIBUTES = {"args", "asctime", "created","exc_info", "exc_text", "filename", "funcName", "levelname", "levelno", "lineno", "message", "module", "msecs", "msg"
                         , "name", "pathname", "process", "processName", "relativeCreated", "stack_info", "thread", "threadName", "taskName"}

class JSONFormatter(logging.Formatter):
    def __init__(self, *, fmt_keys: Optional[dict[str, str]] = None):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        message = self.create_log_dict(record)
        return json.dumps(message, default=str)
    
    def create_log_dict(self, record: logging.LogRecord):
        timestamp = dt.datetime.fromtimestamp(record.created, tz=dt.timezone.utc).isoformat()

        base_fields = {
            "timestamp": timestamp,
            "message" : record.getMessage()
        }

        if record.exc_info is not None:
            base_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            base_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {}
        for key, val in self.fmt_keys.items():
            msg_val = base_fields.pop(val, None)

            if msg_val is not None:
                message[key] = msg_val
            else:
                message[key] = getattr(record, val)
        
        for key, val in record.__dict__.items(): # adding extra attributes that arent part of the default logging record library attributes
            if key not in LOG_RECORD_ATTRIBUTES:
                message[key] = val

        message.update(base_fields)

        return message
