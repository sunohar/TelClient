from loguru import logger
import sys, os
import __main__

# Create logger and set log levels
file_log_level = "INFO"
console_log_level = "DEBUG"

logger.remove()
Log = logger

# Configure console logger
fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>{function: <15}</cyan> | <level>{message: <50}</level>"
Log.add(sys.stdout, level=console_log_level, format=fmt, enqueue=True, backtrace=True, diagnose=True)

# Configure file logger
full_path = __main__.__file__
script_name = os.path.basename(os.path.realpath(full_path))
log_file_name = "./logs/" + script_name[:-3]
Log.add(
    log_file_name + "_{time:YYYYMMDD}.log",
    level=file_log_level,
    format=fmt,
    rotation="00:00",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)
