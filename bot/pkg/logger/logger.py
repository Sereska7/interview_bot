"""Logger module."""

import json
import logging

from colorama import Fore, Style, init

from bot.pkg.settings import settings

init(autoreset=True)


class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for logging, with color coding by log level.

    Attributes:
        LEVEL_COLOR (dict[str, str]): Color mappings for each log level.

    Args:
        fmt_dict (dict[str, str] | None): Mapping of log record attributes to JSON keys.
            Defaults to {"message": "message"}.
        time_format (str): Format string for time display. Default is "%Y-%m-%dT%H:%M:%S".
        msec_format (str): Microsecond formatting string, appended to the end. Default is "%s.%03dZ".
    """

    LEVEL_COLOR: dict[str, str] = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }

    def __init__(
        self,
        fmt_dict: dict[str, str] | None = None,
        time_format: str = "%Y-%m-%dT%H:%M:%S",
        msec_format: str = "%s.%03dZ",
    ) -> None:
        super().__init__()
        self.fmt_dict = fmt_dict if fmt_dict is not None else {"message": "message"}
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None

    def usesTime(self) -> bool:  # noqa N802
        """Check if the formatter uses time in output.

        Returns:
            bool: True if 'asctime' is a part of the output, False otherwise.
        """
        return "asctime" in self.fmt_dict.values()

    def formatMessage(self, record: logging.LogRecord) -> dict[str, str]:  # noqa N802
        """Format the log record as a dictionary based on `fmt_dict` mappings.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            dict[str, str]: Dictionary with formatted log record attributes.

        Raises:
            KeyError: If an unknown attribute is provided in `fmt_dict`.
        """
        return {
            fmt_key: record.__dict__.get(
                fmt_val,
                "",
            )
            for fmt_key, fmt_val in self.fmt_dict.items()
        }

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a JSON string, with color coding based on
        log level.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: JSON-formatted log record with color coding.
        """
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        if hasattr(record, "context"):
            message_dict["context"] = record.context

        color = self.LEVEL_COLOR.get(record.levelname, "")

        if settings.API.ENVIROMENT == "dev":
            colored_message = (
                color
                + json.dumps(
                    message_dict,
                    default=str,
                    indent=4,
                )
                + Style.RESET_ALL
            )
        else:
            colored_message = (
                color
                + json.dumps(
                    message_dict,
                    default=str,
                )
                + Style.RESET_ALL
            )

        return colored_message


class NestedExtraLogger(logging.Logger):
    """Logger that contain extra data dict in record in "extra" attribute."""

    def makeRecord(
        self,
        name,
        level,
        fn,
        lno,
        msg,
        args,
        exc_info,
        func=None,
        extra=None,
        sinfo=None,
    ):
        extra = {"extra": extra or {}}
        return super().makeRecord(
            name,
            level,
            fn,
            lno,
            msg,
            args,
            exc_info,
            func,
            extra,
            sinfo,
        )


logging.setLoggerClass(NestedExtraLogger)


def get_stream_handler() -> logging.StreamHandler:
    """Create and return a stream handler with JSON formatting.

    Returns:
        logging.StreamHandler: Stream handler with JSONFormatter set as the formatter.
    """
    stream_handler = logging.StreamHandler()
    json_formatter = JsonFormatter(
        {
            "timestamp": "asctime",
            "level": "levelname",
            "message": "message",
            "loggerName": "name",
            "fileName": "filename",
            "loggingOnName": "funcName",
            "lineNo": "lineno",
            "processID": "process",
            "extra": "extra",
        },
    )
    stream_handler.setFormatter(json_formatter)
    return stream_handler


def get_logger(name: str) -> logging.Logger:
    """Retrieve or create a logger with a specified name.

    Args:
        name (str): Name for the logger.

    Returns:
        logging.Logger: Configured logger with stream handler and JSON formatting.
    """
    logger = logging.getLogger(name)
    handler_1 = get_stream_handler()
    if not logger.hasHandlers():
        logger.addHandler(handler_1)
    logger.setLevel(settings.LOGGER.LEVEL)
    return logger
