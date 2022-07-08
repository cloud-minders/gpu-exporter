from gpu_exporter.config.env import logging_level
import logging
import toml
import sty
import sys

MAX_LOG_FILE_SIZE = 4  # Gigabytes


class ColorFormatter(logging.Formatter):
    format = "%(asctime)s: [%(levelname)s] %(message)s"

    FORMATS = {
        logging.DEBUG: f"""{sty.fg.magenta} {format} {sty.fg.rs}""",
        logging.INFO: f"""{sty.fg.blue} {format} {sty.fg.rs}""",
        logging.WARNING: f"""{sty.fg.yellow} {format} {sty.fg.rs}""",
        logging.ERROR: f"""{sty.fg.red} {format} {sty.fg.rs}""",
        logging.CRITICAL: f"""{sty.fg.da_red} {format} {sty.fg.rs}""",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


pyproject = toml.load("pyproject.toml")["tool"]["poetry"]
logger = logging.getLogger(__name__)


if logging_level == "DEBUG":
    logger.setLevel(logging.DEBUG)
elif logging_level == "INFO":
    logger.setLevel(logging.INFO)
elif logging_level == "WARN":
    logger.setLevel(logging.WARN)
elif logging_level == "ERROR":
    logger.setLevel(logging.ERROR)
elif logging_level == "CRITICAL":
    logger.setLevel(logging.CRITICAL)


console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(ColorFormatter())
logger.addHandler(console_handler)
