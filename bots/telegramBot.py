import logging
from telegram import Bot
import asyncio

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token):
        self.bot = Bot(token=token)

    async def send_message_async(self, chat_id, text):
        await self.bot.send_message(chat_id=chat_id, text=text)

    def send_message(self, chat_id, text):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_message_async(chat_id, text))

if __name__ == '__main__':
    # Replace 'USER_ID' with the actual user or group chat ID
    user_id = ''
    message_text = 'Hello, this is a test message from your Telegram bot!'
    token = ''
    # Create an instance of the TelegramBot class
    telegram_bot = TelegramBot(token)

    # Send a message using the TelegramBot class
    telegram_bot.send_message(user_id, message_text)
