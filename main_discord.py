from discord import Intents
from discord.ext.commands import Bot

import settings
from src.core.discord.handlers import register_discord_handlers


def init_discord_bot() -> Bot:
    """
    bot = init_discord_bot()
    
    1. call in main (block)
        bot.run(token)
        
    2. call in thread (async, e.g. inner fastapi), ref: https://stackoverflow.com/a/66184381/9422455
        asyncio.create_task(bot.start(token))
    :return:
    """
    intents = Intents.default()
    intents.message_content = True
    bot = Bot(command_prefix="", intents=intents)
    register_discord_handlers(bot)
    return bot


if __name__ == '__main__':
    init_discord_bot().run(settings.DISCORD_BOT_TOKEN)
