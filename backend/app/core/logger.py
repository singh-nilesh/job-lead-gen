import os
import re
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from app.core.config import Settings


def _ensure_dir(path:str) -> str:
    os.makedirs(path, exist_ok=True)
    return path

# logs file path
print(Settings.APP_DIR)
LOGS_DIR = os.path.join(os.path.dirname(Settings.APP_DIR), "logs")

def get_session_log_path() -> str:
    """Helper function for creating Date & Time based dirs and log path
        Returns:str = parent dir. (logs/date/time/)
    """
    date_path = _ensure_dir(os.path.join(
        LOGS_DIR, datetime.now().strftime('%d-%m-%Y')
    ))
    session_log_path = _ensure_dir(os.path.join(
        date_path, datetime.now().strftime('%H:%M:%S')
    ))
    return session_log_path


# logging filters
class FileFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.INFO

class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.INFO


# logger file init
class LazyLogger:
    def __init__(self, logger_name:str):
        self.logger_name = logger_name
        self._logger = None
    
    def _initialize_logger(self):
        if self._logger is None:
            logs_path = get_session_log_path()
            file_path = os.path.join(logs_path, f"{self.logger_name}.log")

            logger = logging.getLogger(f"job-lead-gen.{self.logger_name}")
            logger.setLevel(logging.DEBUG)
            logger.propagate = False

            if not logger.handlers:
                formatter = logging.Formatter(
                    fmt='%(asctime)s - %(name)s:%(lineno)d - %(levelname)s -- %(message)s',
                    datefmt='%H:%M:%S'
                )

                # file handler
                try:
                    file_handler = RotatingFileHandler(
                        filename=file_path,
                        maxBytes=5*1024*1024,
                        backupCount=5
                    )
                    file_handler.setLevel(logging.INFO)
                    file_handler.setFormatter(formatter)
                    file_handler.addFilter(FileFilter())
                    logger.addHandler(file_handler)
                except Exception as e:
                    print(f"Failed to initialize file handler for logger '{self.logger_name}': {e}")
                
                # console handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.INFO)
                console_handler.setFormatter(formatter)
                console_handler.addFilter(ConsoleFilter())
                logger.addHandler(console_handler)

            self._logger = logger
        return self._logger
    
    # proxy methods
    def debug(self, msg, *args, **kwargs):
        logger = self._initialize_logger()
        logger.debug(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        logger = self._initialize_logger()
        logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        logger = self._initialize_logger()
        logger.warning(msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        logger = self._initialize_logger()
        logger.error(msg, *args, **kwargs)
    
    def critical(self, msg, *args, **kwargs):
        logger = self._initialize_logger()
        logger.critical(msg, *args, **kwargs)


# global logger instances

auth_logger = LazyLogger("auth")
db_logger = LazyLogger("database")
api_logger = LazyLogger("api")
service_logger = LazyLogger("service")

if __name__ == "__main__":
    test_logger = LazyLogger("test")
    test_logger.info("This is an info message.")
    test_logger.debug("This is a debug message.")
    test_logger.error("This is an error message.")
    test_logger.critical("This is a critical message.")
