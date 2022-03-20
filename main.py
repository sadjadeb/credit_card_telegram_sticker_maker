from telegram_bot import run_bot
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("log.txt", encoding='utf-8'), logging.StreamHandler()])
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    run_bot()
