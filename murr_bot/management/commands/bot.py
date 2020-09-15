import asyncio
import os
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from django.core.management import BaseCommand

from murr_bot.models import Coub


class Command(BaseCommand):
    help = 'Мурр бот разные выводит штуки'

    def handle(self, *args, **options):
        dp.middleware.setup(ThrottlingMiddleware())
        executor.start_polling(dp)


TOKEN = os.environ.get("BOT_TOKEN", '635496211:AAFGUjMa_NgSQ5c-Cr_19qLnq3HDZigrwx4')

storage = RedisStorage2(host=os.environ.get("REDIS_HOST", 'localhost'), db=5)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.

    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message

        :param message:
        """
        # Get current handler
        handler = current_handler.get()

        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t)

            # Cancel current handler
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):

        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta

        # # Prevent flooding
        if throttled.exceeded_count <= 2:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Команда {message.text} работает 1 раз в {throttled.rate} секунд')

        await message.delete()

        # Sleep.
        await asyncio.sleep(delta)

        # # Check lock status
        thr = await dispatcher.check_key(key)

        # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Unlocked.')


@dp.message_handler(commands=['sexy'])
@rate_limit(30, 'antiflood_sexy')
async def cmd_test(message: types.Message):
    my_ids = list(Coub.objects.values_list('id', flat=True))
    rand_id = random.sample(my_ids, 1)[0]
    coub = Coub.objects.get(id=rand_id)
    await message.reply(f'<a href="{coub.url}">{coub.title}</a>',
                        parse_mode='HTML')


@dp.message_handler(commands=['start'])
@rate_limit(30)
async def cmd_test(message: types.Message):
    await message.reply('Бот работает!')


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_chat_member(message: types.Message):
    reply_message = """Привет, братан!
Добро пожаловать в Мурренган ❤
Вот наш сайт - https://www.murrengan.ru/
Вот как задавать сложные вопросы - https://nometa.xyz/
Еще больше ссылок в описании группы 😘

Сейчас доступна команда - /sexy 
Попробуй ей и поделись впечатлениями 😊

Будь лапочкой  и да пребудет с тобой сила!
    """
    await bot.send_message(chat_id=message.chat.id, text=reply_message)
