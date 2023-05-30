from discord import Intents
from discord.ext.commands import Bot

import settings_discord
from src.core.discord.handlers import register_discord_handlers


def init_discord_bot() -> Bot:
    intents = Intents.default()
    intents.message_content = True
    bot = Bot(command_prefix="", intents=intents)
    register_discord_handlers(bot)
    return bot


if __name__ == '__main__':
    init_discord_bot().run(settings_discord.BOT_TOKEN)
