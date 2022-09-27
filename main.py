import logging
from decouple import config
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardMarkup, KeyboardButton


TOKEN = config('BOT_TOKEN')
BOT_URL = 'https://t.me/juniors_devBot'


bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_message(message.chat.id, f'Здравствуйте {message.chat.first_name}! Выбери, что ты хочешь сделать')