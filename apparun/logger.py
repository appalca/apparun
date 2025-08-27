import logging
import sys

from pydantic_core import ValidationError

logger = logging.getLogger(__name__)


def init_logger():
    """
    Init the logger so that all the logs are saved
    in a file named apparun.log and are redirected on
    the standard output.
    """
    logger.setLevel(level=logging.DEBUG)

    # Format the message in the logs
    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )

    # Write the logs in a file
    file_handler = logging.FileHandler("apparun.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Redirect all the logs to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
