# contains Python runtime events (Exception, etc)
import sys
import logging
from typing import Optional


def error_message_detail(error, error_detail=None):
    try:
        if error_detail is None:
            error_detail = sys  # Fallback to sys if None is passed
        
        _, _, exc_tb = error_detail.exc_info()
        
        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            message = (
                f"\nError occurred in file: {file_name}, "
                f"at line: {exc_tb.tb_lineno}, \nerror: {str(error)}"
            )
        else:
            message = f"\nError occurred: {str(error)} (No traceback info available)"
        return message
    except Exception as e:
        return f"\nFailed to get error details: {str(e)} (Original error: {str(error)})"

# Custom Exception to be used for Logger
class CustomException(Exception):
    """
    Application exception that adds file/line context.

    Args:
        error (Exception | str): Original exception or message.
        error_details (module, optional): sys module to extract traceback.

    Attributes:
        error_message (str): Formatted contextual message.
    """
    def __init__(self, error, error_details=None):
        
        super().__init__(str(error))
        self.error_message = error_message_detail(error, error_details)

    def __str__(self):
        return self.error_message


class ServiceException(Exception):
    """ Base exception for service layer errors.
        Accepts an optional logger; if provided the exception will be logged
    """
    def __init__(
        self,
        message: str,
        logger: Optional[logging.Logger] = None,
        error_details=None,
        level: str = "error",
    ):
        super().__init__(message)
        self.message = message
        self.error_details = error_details or sys
        self._default_level = level
        # only log if a logger was provided
        if logger is not None:
            self.log(logger, level)

    def __str__(self):
        return self.message

    def formatted_message(self) -> str:
        return error_message_detail(self.message, self.error_details)

    def log(self, logger: logging.Logger, level: Optional[str] = None):
        """Log this exception using provided logger. level is a string like 'error'/'warning'/'info'."""
        lvl = level or self._default_level
        log_method = getattr(logger, lvl, logger.error)
        try:
            log_method(self.formatted_message(), exc_info=True)
        except Exception:
            # fallback to logger.error if something goes wrong with chosen method
            logger.error(self.formatted_message(), exc_info=True)


class AlreadyExistsException(ServiceException):
    """ Raised when attempting to create a resource that already exists. """
    pass

class NotFoundException(ServiceException):
    """ Raised when a requested resource is not found. """
    pass

class DatabaseException(ServiceException):
    """ Raised for database-related errors. """
    pass



# Example test block
if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        #logging.info("Divide by Zero")
        raise CustomException("DDivide by Zero")
    


