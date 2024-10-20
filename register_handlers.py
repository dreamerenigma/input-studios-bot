from aiogram import Dispatcher
from filters.filters import register_handlers_filter
from handlers import common


def register_handlers(dp: Dispatcher):
    common.register_handlers_common(dp)
    register_handlers_filter(dp)
