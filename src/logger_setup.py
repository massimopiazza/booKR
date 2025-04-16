import logging
import sys

class GreenFormatter(logging.Formatter):
    GREEN = "\033[32m"
    RESET = "\033[0m"

    def format(self, record):
        # Apply the base formatting, then wrap it in green
        message = super().format(record)
        return f"{self.GREEN}{message}{self.RESET}"

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear any existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = GreenFormatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)