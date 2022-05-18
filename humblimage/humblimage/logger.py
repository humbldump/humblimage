import logging, sys

class CustomFormatter(logging.Formatter):
    
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    purple = "\x1b[35;20m"

    yellow_bold = "\x1b[33;1m"
    red_bold = "\x1b[31;1m"
    green_bold = "\x1b[32;1m"
    grey_bold = "\x1b[38;1m"
    blue_bold = "\x1b[34;1m"
    purple_bold = "\x1b[35;1m"
    reset = "\x1b[0m"
    
    parts = {
        'asctime': '%(asctime)s',
        'name': '%(name)s',
        'levelname': '%(levelname)s',
        'message': '%(message)s',
        'filename': '%(filename)s',
        'lineno': '%(lineno)d'
    }


    FORMATS = {
        logging.DEBUG: f"[{parts['asctime']}] [{grey_bold}{parts['levelname']}{reset}] {parts['message']}",

        logging.INFO: f"[{parts['asctime']}] [{green_bold}{parts['levelname']}{reset}] {green}{parts['message']}{reset}",

        logging.WARNING: f"[{parts['asctime']}] [{yellow_bold}{parts['levelname']}{reset}] {yellow}{parts['message']}{reset}",
        
        logging.ERROR: f"[{parts['asctime']}] [{parts['name']}] [{red_bold}{parts['levelname']}{reset}] {red}{parts['message']}{reset} ({parts['filename']}:{parts['lineno']})",

        logging.CRITICAL: f"[{parts['asctime']}] [{parts['name']}] [{red_bold}{parts['levelname']}{reset}] {red}{parts['message']}{reset} ({parts['filename']}:{parts['lineno']})",

        31: f"[{parts['asctime']}] [{blue_bold}TWEET{reset}] {blue}{parts['message']}{reset}",
        32: f"[{parts['asctime']}] [{purple_bold}DM{reset}] {purple}{parts['message']}{reset}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class customizeLogger():
    def get(self):
        #Set logging class
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        #Set logging to console
        __std_out = logging.StreamHandler(sys.stdout)
        #Set global log level

        #Apply logging format
        __std_out.setFormatter(CustomFormatter())

        #Add handler to logger
        logger.addHandler(__std_out)
        return logger