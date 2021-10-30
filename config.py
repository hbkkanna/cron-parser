import logging
import sys


class Config():
    def __init__(self, loglevel):
        logger = logging.getLogger("Cron-Parser")
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.setLevel(loglevel)
        self.logger = logger

    def get_logger(self):
        return self.logger


config = Config(logging.INFO)
