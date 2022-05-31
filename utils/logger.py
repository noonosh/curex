import os
import logging
import dotenv

dotenv.load_dotenv()

DEBUG = os.getenv('DEBUG', False)


logging.basicConfig(
    filename='log.log' if not DEBUG else None,
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if DEBUG else logging.INFO)

logger = logging.getLogger(__name__)
