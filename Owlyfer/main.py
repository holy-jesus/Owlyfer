import asyncio

import bot.handlers
from bot.loader import bot, dp
from utils.log_worker import Logger
from utils.posts_worker import send_delayed_posts
from db import create_tables


if __name__ == "__main__":
    Logger.info("Bot started")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(create_tables())
    loop.create_task(send_delayed_posts())
    loop.run_until_complete(dp.start_polling(bot))
    Logger.info("Bot stopped")
