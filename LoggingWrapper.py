"""
Logging Wrapper

This class is meant to be used as a quick connect utility wrapper that can be configured
for consistent use while keeping code clean.
"""
import logging
import logging.handlers
import os


LEVELS = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class LoggingWrapper:
    def __init__(self, logname, stream_level="INFO", file_level="DEBUG"):
        self.logname = logname
        if not os.path.exists(self.logname):
            self.logname = open(self.logname, "w+")
        self.stream_level = stream_level
        self.file_level = file_level

        self.logname_split = self.logname.split(".")[0]
        self.logger = logging.getLogger(self.logname_split)
        self.logger.setLevel(LEVELS.get(stream_level, "INFO"))
        self.formatter = [None] * 2
        self.formatter_logger()

    def print_logger(self):
        print(dir(self.logger.handle))

    def formatter_logger(
        self,
        format_string="%(asctime)s | %(module)s:%(funcName)s():%(lineno)s | %(levelname)s: %(message)s",
        handler="both",
    ):
        assert handler in [
            "stream",
            "file",
            "both",
        ], f"handler {handler} not 'stream', 'file', or 'both'."
        if handler == "stream":
            self.formatter[0] = logging.Formatter(format_string)
        elif handler == "file":
            self.formatter[1] = logging.Formatter(format_string)
        else:
            self.formatter[0] = self.formatter[1] = logging.Formatter(format_string)
        self.update_logger(handler)

    def stream_handle_setup(self, stream_level="INFO"):
        assert self.check_level(stream_level)
        if self.stream_level != stream_level:
            self.logger.debug(
                f"Old stream logger: {self.stream_level}, New stream logger: {stream_level}"
            )
            self.stream_level = stream_level
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(LEVELS.get(self.stream_level, logging.INFO))
        stream_handler.setFormatter(self.formatter[0])
        self.logger.addHandler(stream_handler)

    def file_handle_setup(self, file_level="DEBUG"):
        assert self.check_level(file_level)
        if self.file_level != file_level:
            self.logger.debug(
                f"Old file logger: {self.file_level}, New file logger: {file_level}"
            )
            self.file_level = file_level
        file_handler = logging.handlers.RotatingFileHandler(filename=self.logname)
        file_handler.setLevel(LEVELS.get(self.file_level, logging.DEBUG))
        file_handler.setFormatter(self.formatter[1])
        self.logger.addHandler(file_handler)

    def check_level(self, level):
        valid_level = True
        if not LEVELS.get(level):
            self.logger.error(f"Level {level} not in logger levels.")
            valid_level = False
        return valid_level

    def update_logger(self, handler):
        assert handler in [
            "stream",
            "file",
            "both",
        ], f"handler {handler} not 'stream', 'file', or 'both'."
        if handler == "stream":
            self.stream_handle_setup()
        elif handler == "file":
            self.file_handle_setup()
        else:
            self.stream_handle_setup()
            self.file_handle_setup()

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
