import os
from dotenv import load_dotenv
from src.main.Bot import Bot

if __name__ == "__main__":
    load_dotenv()
    bot = Bot()
    bot.run(os.getenv('BOT_TOKEN'))
