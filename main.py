import logging
import logging.handlers
import os

import requests

logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        "status.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    try:
        r = requests.get(
            'https://weather.talkpython.fm/api/weather/?city=Berlin&country=DE',
            timeout=10  # 10 second timeout
        )
        r.raise_for_status()  # Raises HTTPError for bad status codes
        data = r.json()
        temperature = data.get("forecast", {}).get("temp")
        if temperature is not None:
            logger.info(f'Weather in Berlin: {temperature}')
        else:
            logger.warning("Temperature data not found in API response")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch weather data: {e}")
    except (KeyError, ValueError) as e:
        logger.error(f"Failed to parse weather data: {e}")