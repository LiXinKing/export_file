import logging

LOG_PATH = ""

def debug_log(msg):
    logging.basicConfig(filename=LOG_PATH + "\\" + 'export.log',level=logging.DEBUG)
    logging.debug(msg)

def warning_log(msg):
    logging.basicConfig(filename=LOG_PATH + "\\" + 'export.log',level=logging.WARNING)
    logging.warning(msg)

def config_log_path(path):
    global LOG_PATH
    LOG_PATH = path
