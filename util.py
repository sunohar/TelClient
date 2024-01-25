from loguru import logger
import sys, os
import __main__


def make_filter(name):
    def filter(record):
        return record["extra"].get("name") == name

    return filter


# Create logger and set log levels
file_log_level = "INFO"
console_log_level = "INFO"

logger.remove()
# Log = logger.bind(name="default")
# Log2 = logger.bind(name="all")

# Configure console logger
fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>{function: <15}</cyan> | <level>{message: <50}</level>"
logger.add(sys.stdout, level=console_log_level, format=fmt, enqueue=True, backtrace=True, diagnose=True)
# Log2.add(sys.stdout, level=console_log_level, format=fmt, filter="all", enqueue=True, backtrace=True, diagnose=True)
# Configure file logger
full_path = __main__.__file__
script_name = os.path.basename(os.path.realpath(full_path))
log_file_name = "./logs/" + script_name[:-3]
logger.add(
    log_file_name + "_{time:YYYYMMDD}.log",
    level=file_log_level,
    filter=make_filter("default"),
    format=fmt,
    rotation="00:00",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

logger.add(
    "./logsAll/LogAll_{time:YYYYMMDD}.log",
    level=file_log_level,
    filter=make_filter("all"),
    format=fmt,
    rotation="00:00",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

Log = logger.bind(name="default")
Log2 = logger.bind(name="all")
