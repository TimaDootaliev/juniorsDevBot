import logging
from decouple import config
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery
from keyboards import Keyboard


TOKEN = config('BOT_TOKEN')
BOT_URL = 'https://t.me/juniors_devBot'


logging.basicConfig(level=logging.DEBUG)


bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_message(
        message.chat.id, 
        f'Здравствуйте, {message.chat.first_name}! Выбери, что ты хочешь сделать', 
        reply_markup=Keyboard.get_keyboard()
        )
    # print(message)



@dp.callback_query_handler(lambda callback_query: True)
async def action_on_query_data(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    data = callback_query.data
    if data == 'send_check':
        await bot.send_message(chat_id, 'Отправьте чек и информацию о себе в следующем формате\n')
        await bot.send_photo(chat_id, open('example.jpeg', 'rb'))
        if callback_query.from_user.username:
            await bot.send_message(chat_id, 'ФИО: Джон Ватсон\nПочта: john.watson@gmail.com')
        else:
            await bot.send_message(chat_id, 'ФИО: Джон Ватсон\nПочта: john.watson@gmail.com\nTelegram: @johnwatson')
    elif data == 'faq':
        await bot.send_message(
            chat_id, 
            'Выбери вопрос', 
            reply_markup=Keyboard.get_faq_keyboard()
            )


@dp.message_handler(content_types=['photo'])
async def send_check_to_admin(message: Message):
    await bot.send_photo('294919372', message.photo[0].file_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)