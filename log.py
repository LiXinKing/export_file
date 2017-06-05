import logging

def debug_log(msg):
    logging.basicConfig(filename='export.log',level=logging.DEBUG)
    logging.debug(msg)

def warning_log(msg):
    logging.basicConfig(filename='export.log',level=logging.WARNING)
    logging.warning(msg)
