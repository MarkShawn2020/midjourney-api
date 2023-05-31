import asyncio

import aiofiles

import settings
from src.lib.exceptions import BannedPromptError


async def loads_banned_words():
    prompt = set()
    async with aiofiles.open(settings.MIDJOURNEY_BANNED_WORDS_FILE_PATH, "r") as r:
        for line in await r.readlines():
            prompt.add(line.strip())
    
    return prompt


BANNED_PROMPTS = asyncio.run(loads_banned_words())


def check_banned(prompt: str):
    words = set(w.lower() for w in prompt.split())
    if len(words & BANNED_PROMPTS) != 0:
        raise BannedPromptError(f"banned prompt: {prompt}")
