import logging
import logging.handlers


class Logger(object):
    FORMAT = "%(asctime)s %(filename)s [%(levelname)s] %(message)s"
    LOG_LEVEL = logging.DEBUG

    def __init__(self, name):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(self.LOG_LEVEL)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.LOG_LEVEL)
        stream_handler.setFormatter(logging.Formatter(self.FORMAT))
        self.__logger.addHandler(stream_handler)

    def set_logfile(self, filename):
        # file_handler = logging.FileHandler(filename, mode='a', encoding='utf-8')
        file_handler = logging.handlers.RotatingFileHandler(
            filename, mode='a', encoding='utf-8', maxBytes=100000, backupCount=10)
        file_handler.setLevel(self.LOG_LEVEL)
        file_handler.setFormatter(logging.Formatter(self.FORMAT))
        self.__logger.addHandler(file_handler)

    @property
    def logger(self):
        return self.__logger
