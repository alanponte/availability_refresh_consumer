import logging
import sys
from logging import config as logging_config
from typing import Optional

SERVICE_NAME = 'availability_refresh_consumer'


def get_logger() -> logging.Logger:
    """Return the logger instance for this Daemon."""
    return SvcLogger(SERVICE_NAME).log


class SvcLogger:
    """Handles logging for fp service code."""
    __configured = False

    def __init__(self, name: Optional[str] = None):
        """Initializes SvcLogger class through logging configuration and
        creation of a Logger instance variable.

        Args:
            name (str): the __name__ of the module being logged. Must match
            one of the configured loggers ('src', 'fp_common', or 'cron_jobs')
            in order for the log entry to be captured.

        Example usage:
            Create a module-level instance of the logger using
            the module name attribute, and reference where needed:
                _log= SvcLogger(__name__).log
                _log.info("informational message")
        """
        validated = (name is not None) and (
            'availability_refresh_consumer' in name or
            '__main__' in name
        )

        if not validated:
            raise ValueError(
                f"Argument 'name' {name} must be the __name__ attribute.")

        self.logger = logging.getLogger(name if name else __name__)

    @property
    def log(self):
        """Contains a reference to the Logger instance variable.

        Returns:
            Logger: a configured Logger instance

        Example usage:
            _log= SvcLogger(__name__).log
            _log.info("informational message")
            _log.debug("debug message")
        """
        return self.logger

    @classmethod
    def configure(cls):
        """Configures python logging using the settings of the included
        dictionary. This method only needs to be called once.

        This specific configuration will stream json logging to stdout.
        """
        if cls.__configured:
            return

        configuration: dict = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'json': {
                    'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                    'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
                }
            },
            'handlers': {
                'json': {
                    'level': 'DEBUG',
                    'formatter': 'json',
                    'class': 'logging.StreamHandler',
                    'stream': sys.stdout
                }
            },
            'loggers': {
                'geotab_sync_daemon': {
                    'handlers': ['json'],
                    'level': 'DEBUG',
                    'propagate': True
                },
                '__main__': {
                    'handlers': ['json'],
                    'level': 'DEBUG',
                    'propagate': True
                }
            }
        }
        logging_config.dictConfig(configuration)
        cls.__configured = True


SvcLogger.configure()
