import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from app.core.config import Settings


def _ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


# logs directory
LOGS_DIR = os.path.join(os.path.dirname(Settings.APP_DIR), "logs")


def get_session_log_path() -> str:
    """Helper function for creating Date & Time based dirs and log path"""
    date_path = _ensure_dir(os.path.join(
        LOGS_DIR, datetime.now().strftime('%d-%m-%Y')
    ))
    session_log_path = _ensure_dir(os.path.join(
        date_path, datetime.now().strftime('%H-%M-%S')
    ))
    return session_log_path


# filters
class FileFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.DEBUG  # keep all


class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR


class LazyLogger:
    """Lazy-initialized logger with rotating file handler and per-session logs."""

    def __init__(self, logger_name: str):
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
                # Updated formatter: shows full path of the module
                formatter = logging.Formatter(
                    fmt='%(asctime)s | %(levelname)-3s | %(module)s.%(funcName)s:%(lineno)d | %(message)s',
                    datefmt='%H:%M:%S'
                    )

                # File handler
                try:
                    file_handler = RotatingFileHandler(
                        filename=file_path,
                        maxBytes=5 * 1024 * 1024,
                        backupCount=5,
                        encoding='utf-8'
                    )
                    file_handler.setLevel(logging.DEBUG)  # capture ALL levels
                    file_handler.setFormatter(formatter)
                    file_handler.addFilter(FileFilter())
                    logger.addHandler(file_handler)
                except Exception as e:
                    print(f"Failed to initialize file handler for logger '{self.logger_name}': {e}")

                # Console handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.WARNING)
                console_handler.setFormatter(formatter)
                console_handler.addFilter(ConsoleFilter())
                logger.addHandler(console_handler)

            self._logger = logger

        return self._logger

        # proxy methods
    def debug(self, msg, *args, **kwargs):
        self._initialize_logger().debug(msg, *args, stacklevel=2, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._initialize_logger().info(msg, *args, stacklevel=2, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._initialize_logger().warning(msg, *args, stacklevel=2, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._initialize_logger().error(msg, *args, stacklevel=2, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._initialize_logger().critical(msg, *args, stacklevel=2, **kwargs)


# Global logger instances
auth_logger = LazyLogger("auth")
db_logger = LazyLogger("database")
api_logger = LazyLogger("api")
service_logger = LazyLogger("service")


if __name__ == "__main__":
    test_logger = LazyLogger("test")
    test_logger.debug("This is a DEBUG message.")
    test_logger.info("This is an INFO message.")
    test_logger.warning("This is a WARNING message.")
    test_logger.error("This is an ERROR message.")
    test_logger.critical("This is a CRITICAL message.")
