import logging
import logging.handlers
import sys

import colorlog

from config import DEBUG

GENERIC_ERROR = 'Our bad - please contact support for further assistance'

if DEBUG:
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s[%(levelname)s]%(reset)s %(name)s: %(message)s'))
    handler.setLevel(logging.DEBUG)
else: 
    formatter = logging.Formatter(logging.BASIC_FORMAT) # Update later for deployment
    handler = logging.handlers.WatchedFileHandler('log.txt')
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

root = logging.getLogger()
root.addHandler(handler)
