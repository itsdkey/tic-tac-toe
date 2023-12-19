###########
# LOGGING #
###########
from pathlib import Path

LOGGING = {
    "version": 1,
    "formatters": {
        "default": {
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "[{asctime}][{name}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "local": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "__main__": {
            "level": "DEBUG",
            "handlers": ["local"],
            "propagate": False,
        },
        "desktop.elements": {
            "level": "DEBUG",
            "handlers": ["local"],
            "propagate": False,
        },
    },
}

STATICS_DIR = Path(__file__).parent / "statics"
