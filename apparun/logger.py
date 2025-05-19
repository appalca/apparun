import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# Format the message in the logss
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
