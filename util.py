import yaml
import logging, os
from logging.handlers import RotatingFileHandler
import __main__


class ConsoleFormatter(logging.Formatter):

    grey = "\x1b[38;21m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    bold_red = "\x1b[31;1m"
    bold_green = "\x1b[32;1m"
    green = "\x1b[32m"
    reverse = "\x1b[7m"
    bold = "\x1b[1m"
    underline = "\x1b[4m"
    reset = "\x1b[0m"
    format_str = "{asctime}.{msecs:03.0f} - {funcName:^16s} - {lineno:04d} - {levelname:^9s} - {message}"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: green + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + reverse + format_str + reset,
    }

    def set_format_str(self, str):
        self.FORMATS = {
            logging.DEBUG: self.grey + str + self.reset,
            logging.INFO: self.green + str + self.reset,
            logging.WARNING: self.yellow + str + self.reset,
            logging.ERROR: self.red + str + self.reset,
            logging.CRITICAL: self.bold_red + self.reverse + str + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style="{", datefmt="%Y-%b-%d %H:%M:%S")
        return formatter.format(record)


class TICSLogger:
    def __init__(self, logger=None, filename=None, dir=None, max_size="5242880", max_num="10", rich_console=False):

        if filename is None:
            full_path = __main__.__file__
            script_name = os.path.basename(os.path.realpath(full_path))
            filename = script_name[:-3] + ".log"

        if dir is None:
            full_path = __main__.__file__
            dir = os.path.dirname(os.path.realpath(full_path))

        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)

        if logger is None:
            full_path = __main__.__file__
            script_name = os.path.basename(os.path.realpath(full_path))
            logger = script_name[:-3]

        self.format_str = "{asctime}.{msecs:03.0f} | {funcName:^16s} | {lineno:04d} | {levelname:^9s} | {message}"
        self.style = "{"
        self.datefmt = "%Y-%m-%d %H:%M:%S"
        self.log_formatter = logging.Formatter(self.format_str, style=self.style, datefmt=self.datefmt)

        # Set console formatting
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)

        if rich_console:
            console_formatter = ConsoleFormatter()
            console_formatter.set_format_str(self.format_str)
            self.console_handler.setFormatter(console_formatter)
        else:
            self.console_handler.setFormatter(self.log_formatter)

        # Try to get configurations from os environment variables for file logging
        log_file_name = os.environ["LOG_FILENAME"] if "LOG_FILENAME" in os.environ else filename
        directory = os.environ["LOG_FILE_DIR"] if "LOG_FILE_DIR" in os.environ else dir
        max_filesize_str = os.environ["LOG_MAXSIZE"] if "LOG_MAXSIZE" in os.environ else max_size
        backupCount_str = os.environ["LOG_BACKUP_COUNT"] if "LOG_BACKUP_COUNT" in os.environ else max_num
        loggername = os.environ["LOGGER_NAME"] if "LOGGER_NAME" in os.environ else logger
        try:
            max_filesize = int(max_filesize_str)
        except:
            max_filesize = 5242880
        try:
            backupCount = int(backupCount_str)
        except:
            backupCount = 10
        logFile = os.path.join(directory, log_file_name) if os.path.exists(directory) else log_file_name

        self.file_handler = RotatingFileHandler(
            logFile,
            mode="a",
            maxBytes=max_filesize,  # Max log file size: 5 MB (5242880 B) (5*1024*1024)
            backupCount=backupCount,
            encoding="utf-8",
            delay=0,
        )
        self.file_handler.setFormatter(self.log_formatter)
        self.file_handler.setLevel(logging.DEBUG)

        self.get_log = logging.getLogger(loggername)
        self.get_log.setLevel(logging.DEBUG)

        self.get_log.addHandler(self.file_handler)
        self.get_log.addHandler(self.console_handler)

    def set_dbglevel_debug(self):
        self.get_log.setLevel(logging.DEBUG)

    def set_dbglevel_info(self):
        self.get_log.setLevel(logging.INFO)

    def set_dbglevel_warning(self):
        self.get_log.setLevel(logging.WARNING)

    def set_dbglevel_error(self):
        self.get_log.setLevel(logging.ERROR)

    def set_dbglevel_critical(self):
        self.get_log.setLevel(logging.CRITICAL)

    # set level of console logging
    def console_dbglevel_debug(self):
        self.console_handler.setLevel(logging.DEBUG)

    def console_dbglevel_info(self):
        self.console_handler.setLevel(logging.INFO)

    def console_dbglevel_warning(self):
        self.console_handler.setLevel(logging.WARNING)

    def console_dbglevel_error(self):
        self.console_handler.setLevel(logging.ERROR)

    def console_dbglevel_critical(self):
        self.console_handler.setLevel(logging.CRITICAL)

    # set level of logfile logging
    def logfile_dbglevel_debug(self):
        self.file_handler.setLevel(logging.DEBUG)

    def logfile_dbglevel_info(self):
        self.file_handler.setLevel(logging.INFO)

    def logfile_dbglevel_warning(self):
        self.file_handler.setLevel(logging.WARNING)

    def logfile_dbglevel_error(self):
        self.file_handler.setLevel(logging.ERROR)

    def logfile_dbglevel_critical(self):
        self.file_handler.setLevel(logging.CRITICAL)

    def set_maxSize(self, maxBytes):
        self.file_handler.maxBytes = maxBytes

    def set_backupCount(self, backupCount):
        self.file_handler.backupCount = backupCount

    def console_dbglevel(self, levelname):
        if levelname.lower() == "debug":
            self.console_handler.setLevel(logging.DEBUG)
        elif levelname.lower() == "info":
            self.console_handler.setLevel(logging.INFO)
        elif levelname.lower() == "warning":
            self.console_handler.setLevel(logging.WARNING)
        elif levelname.lower() == "error":
            self.console_handler.setLevel(logging.ERROR)
        elif levelname.lower() == "critical":
            self.console_handler.setLevel(logging.CRITICAL)
        else:
            print(f"Level is not defined in console_dbglevel")

    def file_dbglevel(self, levelname):
        if levelname.lower() == "debug":
            self.file_handler.setLevel(logging.DEBUG)
        elif levelname.lower() == "info":
            self.file_handler.setLevel(logging.INFO)
        elif levelname.lower() == "warning":
            self.file_handler.setLevel(logging.WARNING)
        elif levelname.lower() == "error":
            self.file_handler.setLevel(logging.ERROR)
        elif levelname.lower() == "critical":
            self.file_handler.setLevel(logging.CRITICAL)
        else:
            print(f"Level is not defined in file_dbglevel")


def read_config(filename):
    config = {}
    try:
        with open(filename, "r") as cfg:
            config = yaml.safe_load(cfg)
    except Exception as e:
        print(f"Unable to read config file. Error: {e}")

    print(f"Configuration read for {filename} complete.")
    return config


# CONFIG = read_config("./config/config.yaml")
# DBMAP = read_config("./config/db_map.yaml")

# Create logger and set log levels
file_log_level = "debug"
console_log_level = "debug"
rich_console = False

Logger = TICSLogger(dir="./logs", rich_console=rich_console)
Log = Logger.get_log
Logger.console_dbglevel(console_log_level)
Logger.file_dbglevel(file_log_level)
