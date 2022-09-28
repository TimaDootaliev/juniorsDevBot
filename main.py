import logging
from decouple import config
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards import kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


TOKEN = config('BOT_TOKEN')
ADMIN_ID = config('ADMIN_ID')


logging.basicConfig(level=getattr(logging, config('MODE'), logging.DEBUG))


class Form(StatesGroup):
    image = State()
    data = State()


storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_message(
        message.chat.id, 
        f'Здравствуйте, {message.chat.first_name}! Выбери, что ты хочешь сделать', 
        reply_markup=kb.get_keyboard()
        )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'faq')
async def action_on_query_data(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    await bot.send_message(
            chat_id, 
            'Выбери вопрос', 
            reply_markup=kb.get_faq_keyboard()
            )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'send_check')
async def action_on_send_check(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    await bot.send_message(chat_id, 'Отправьте чек и информацию о себе в следующем формате\n')
    try:
        photo = open('example.jpeg', 'rb')
        if callback_query.from_user.username:
            await bot.send_photo(
                chat_id, photo=photo, 
                caption='ФИО: Джон Ватсон\nПочта: john.watson@gmail.com\n\nОтменить операцию /cancel'
                )
        else:
            await bot.send_photo(
                chat_id, 
                photo=photo,
                caption='ФИО: Джон Ватсон\nПочта: john.watson@gmail.com\nTelegram: @johnwatson\n\nОтменить операцию /cancel'
                )
    finally:
        photo.close()
    await Form.data.set()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await bot.send_message(message.chat.id, 'Выберите другую операцию', reply_markup=kb.get_keyboard())


@dp.message_handler(content_types=[ContentType.PHOTO, ContentType.TEXT], state=Form.data)
async def process_data(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        data['info'] = message.caption
    await state.finish()
    if message.from_user.username:
        await bot.send_photo(
            ADMIN_ID, 
            photo=data['photo'], 
            caption=data['info'] + f'\n@{message.from_user.username}')
    else:
        await bot.send_photo(
            ADMIN_ID, 
            photo=data['photo'], 
            caption=data['info'])
    await bot.send_message(message.chat.id, 'Спасибо!', reply_markup=kb.get_keyboard())
    

@dp.callback_query_handler(lambda callback_query: callback_query.data=='how_to_start')
async def how_to_start(cq: CallbackQuery):
    msg = """
    Как начать? 

Чтобы начать прокачку: 
1. Необходимо внести оплату 830 сомов; 
    Реквизиты: Мбанк 0703666656, Элсом 0501619690; 
2. Прикрепить чек сюда в сообщениях и отправить
3. Добавим в группу в течение 1 часа

Внимание!
4. Не надо ждать даты старта, у нас нет потоков или даты старта групп.
5. Можно приступить к программе в любое удобное для вас время.
    """
    await bot.send_message(cq.message.chat.id, msg, reply_markup=kb.get_faq_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data=='about_program')
async def about_program(cq: CallbackQuery):
    msg = """
    Как проходит программа? 

1. Вы получаете детально расписанные технические задания проекта. Все технологии, которые заложены в проекте, утверждены компаниями. Все проекты составлены опытными middle разработчикам. 
2. Вы будете не одни, вас ждет наше дружелюбное сообщество. Нас уже более 50 junior разработчиков. 
3. Принимаете участие на мероприятиях с опытными разработчиками, с парных собеседованиях, обсуждаете проекты и учитесь друг у друга. Если у вас сложности, у вас будет у кого спросить. 
4. Программа полностью онлайн. 
5. Программа будет идти до вашего трудоустройства, и даже после. 
    """
    await bot.send_message(cq.message.chat.id, msg, reply_markup=kb.get_faq_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data=='when')
async def date_handler(cq: CallbackQuery):
    msg = """
    Когда начнется?
Можете приступать прямо сейчас. У нас нет понятия старта программы. Нет потоков. Желающие могут начать когда удобно. 
    """
    await bot.send_message(cq.message.chat.id, msg, reply_markup=kb.get_faq_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data=='price')
async def price_handler(cq: CallbackQuery):
    msg = """
    Сколько стоит?

Стоимость участие $30, или 2490 сомов. Первым 100 пользователям - $10, то есть 830 сомов. 
    
Если вы это читаете, значит еще успеваете купить по $10. 

Это единоразовый платеж, других обязательных оплат нет. Также, нет ежемесячной платы за подписку.
    """
    await bot.send_message(cq.message.chat.id, msg, reply_markup=kb.get_faq_keyboard())




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)