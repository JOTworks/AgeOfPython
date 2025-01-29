import logging


class ColorFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + "%(levelname)s - %(message)s" + reset,
        logging.INFO: grey + "%(levelname)s - %(message)s" + reset,
        logging.WARNING: yellow + "%(levelname)s - %(message)s" + reset,
        logging.ERROR: red + "%(levelname)s - %(message)s" + reset,
        logging.CRITICAL: bold_red
        + "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Create a logger and set its level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a handler and set its formatter
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter())

# Add the handler to the logger
logger.addHandler(handler)
