from fastapi.datastructures import Headers
from exceptions import LoggerException
import json
import logging
from logging.handlers import RotatingFileHandler
import os

from typing import Any, Callable, Dict, Optional

# This JSON log formatter is taken from Bogdan Mircea on Stack Overflow:
#   https://stackoverflow.com/questions/50144628/python-logging-into-file-as-a-dictionary-or-json
class JSONFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.

    @param dict fmt_dict: Key: logging format attribute pairs. Defaults to {"message": "message"}.
    @param str time_format: time.strftime() format string. Default: "%Y-%m-%dT%H:%M:%S"
    @param str msec_format: Microsecond formatting. Appended at the end. Default: "%s.%03dZ"
    """
    def __init__(self, fmt_dict: dict = None, time_format: str = "%Y-%m-%dT%H:%M:%S", msec_format: str = "%s.%03dZ"):
        self.fmt_dict = fmt_dict if fmt_dict is not None else {"message": "message"}
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None

    def usesTime(self) -> bool:
        """
        Overwritten to look for the attribute in the format dict values instead of the fmt string.
        """
        return "asctime" in self.fmt_dict.values()

    def formatMessage(self, record) -> dict:
        """
        Overwritten to return a dictionary of the relevant LogRecord attributes instead of a string. 
        KeyError is raised if an unknown attribute is provided in the fmt_dict. 
        """
        return {fmt_key: record.__dict__[fmt_val] for fmt_key, fmt_val in self.fmt_dict.items()}

    def format(self, record) -> str:
        """
        Mostly the same as the parent's class method, the difference being that a dict is manipulated and dumped as JSON
        instead of a string.
        """
        record.message = record.getMessage()
        
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(message_dict, default=str)

class JSONLogger:
    def __init__(
        self,
        log_file_name: str, 
        log_dir: str = "",
        log_level: int = logging.INFO
    ) -> None:
        self.logger: logging.Logger = logging.Logger(__name__)
        self.logger.setLevel(log_level)

        log_formatter: JSONFormatter = JSONFormatter({
            "level": "levelname", 
            "data": "message", 
            "loggerName": "name", 
            "processName": "processName",
            "processID": "process", 
            "threadName": "threadName", 
            "threadID": "thread",
            "timestamp": "asctime"
        })

        if not os.path.isdir(log_dir) and log_dir != "":
            try:
                os.mkdir(log_dir)
            except:
                raise LoggerException(f"Could not create logging directory {log_dir}")

        file_handler: RotatingFileHandler = RotatingFileHandler(
            filename=os.path.join(log_dir, log_file_name),
            mode="a",
            maxBytes=1e6,
            backupCount=3,
            encoding=None,
            delay=False
        )
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        self.logger_map: Dict[str, Callable[..., None]] = {
            "DEBUG": self.logger.debug,
            "INFO": self.logger.info,
            "WARNING": self.logger.warning,
            "ERROR": self.logger.error,
            "CRITICAL": self.logger.critical
        }

    def log(self, message: object, level: str = "DEBUG") -> None:
        try:
            self.logger_map[level](message)
        except:
            pass

    async def log_incoming_request(
        self,
        request_id: str,
        request_type: str,
        body: bytes = b'',
        host: Optional[str] = None,
        port: Optional[str] = None,
        headers: Optional[Headers] = None,
        cookies: Optional[Dict[str, str]] = None,
        level: str = "INFO"
    ) -> None:
        logging_data: Dict[str, Any] = {
            "log_type": "request",
            "request_id": request_id,
            "request_type": request_type,
            "origin": {
                "host": host,
                "port": port
            },
            "headers": dict(headers),
            "cookies": dict(cookies),
            "request_body": json.loads(body.decode('utf-8'))
        }
        self.log(message=logging_data, level=level)

    async def log_outgoing_response(
        self,
        request_id: str,
        request_type: str,
        outgoing_response: Any,
        level: str = "INFO"
    ) -> None:
        logging_data = {
            "log_type": "response",
            "request_id": request_id,
            "request_type": request_type,
            "response": outgoing_response
        }
        self.log(message=logging_data, level=level)
