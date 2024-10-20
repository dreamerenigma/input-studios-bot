from aiogram import Router, types
from aiogram.filters import Command
from ban_words import ban_words
from filters.filters import ProfanityFilter, handle_profanity
from handlers.messages import welcome_text

router = Router()

profanity_filter = ProfanityFilter(ban_words)


async def start_command(message: types.Message):
    await message.answer(welcome_text, parse_mode='HTML', disable_web_page_preview=True)


async def help_command(message: types.Message):
    await message.answer(welcome_text, parse_mode='HTML', disable_web_page_preview=True)


def register_handlers_common(dp):
    router.message.register(start_command, Command(commands=["start"]))
    router.message.register(help_command, Command(commands=["help"]))
    router.message(profanity_filter)(handle_profanity)
    dp.include_router(router)
