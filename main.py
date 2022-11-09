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
    name = State()
    phone_number = State()
    email = State()
    stack = State()
    tg = State()


storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state='*')
async def start(message: Message, state: FSMContext):
    await bot.send_message(
        message.chat.id, 
        f'Здравствуйте, {message.chat.first_name}!', 
        reply_markup=kb.get_keyboard()
        )
    await bot.send_message(
        message.chat.id, text='Выбери, что ты хочешь сделать', 
        reply_markup=kb.send_check_button())
    await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'faq')
async def action_on_query_data(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    await bot.send_message(
            chat_id, 
            'Выбери вопрос', 
            reply_markup=kb.get_faq_keyboard()
            )


@dp.message_handler(lambda message: message.text == '💵 Отправить чек')
async def action_on_send_check(message: Message):
    chat_id = message.chat.id
    if message.from_user.username:
        await bot.send_message(
            chat_id, 
            text='Пожалуйста, отправьте фото чека')
    await Form.image.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'send_check')
async def action_on_send_check(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    if callback_query.from_user.username:
        await bot.send_message(
            chat_id, 
            text='Пожалуйста, отправьте фото чека',
            reply_markup=kb.cancel_button()
            )
    await Form.image.set()


@dp.message_handler(lambda message: message.text == 'Отмена операции',state='*')
@dp.message_handler(Text(equals='Отмена операции', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await bot.send_message(message.chat.id, 'Выберите другую операцию', reply_markup=kb.get_keyboard())

    
@dp.message_handler(content_types=ContentType.PHOTO, state=Form.image)
async def process_image(message: Message, state: FSMContext):
    """
    Process user image
    """
    print(message)
    async with state.proxy() as data:
        data['image'] = message.photo[0].file_id

    await Form.next()
    await message.reply("Пожалуйста, отправьте Ваше имя и фамилию")


@dp.message_handler(content_types=ContentType.TEXT, state=Form.name)
async def process_name(message: Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Укажите Ваш номер телефона")


@dp.message_handler(content_types=ContentType.TEXT, state=Form.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    """
    Process user phone_number
    """
    async with state.proxy() as data:
        data['phone_number'] = message.text

    await Form.next()
    await message.reply("Укажите Вашу почту")


@dp.message_handler(content_types=ContentType.TEXT, state=Form.email)
async def process_email(message: Message, state: FSMContext):
    """
    Process user email
    """
    async with state.proxy() as data:
        data['email'] = message.text

    await Form.next()
    await message.reply("Укажите Ваш стэк (навыки, которыми Вы уже владеете)")


@dp.message_handler(content_types=ContentType.TEXT, state=Form.stack)
async def process_stack(message: Message, state: FSMContext):
    """
    Process user stack
    """
    async with state.proxy() as data:
        data['stack'] = message.text
    if message.from_user.username:
        await state.finish()
        await message.reply("Спасибо! Скоро мы добавим Вас в группу", reply_markup=kb.get_faq_keyboard())
        await bot.send_photo(
                ADMIN_ID, 
                photo=data['image'], 
                caption=f"{data['name']}\n{data['phone_number']}\n{data['stack']}\n{data['email']}\n@{message.from_user.username}"
                )
    else:
        await Form.next()
        await message.reply("Укажите ваш профиль Telegram (@myusername)")


@dp.message_handler(content_types=ContentType.TEXT, state=Form.tg)
async def process_tg_username(message: Message, state: FSMContext):
    """
    Process user username
    """
    async with state.proxy() as data:
        data['username'] = message.text

    await state.finish()
    await message.reply("Спасибо! Скоро мы добавим Вас в группу", reply_markup=kb.get_faq_keyboard())
    await bot.send_photo(
            ADMIN_ID, 
            photo=data['image'], 
            caption=f"{data['name']}\n{data['stack']}\n{data['email']}\n@{message.from_user.username}\n{data['username']}"
            )




@dp.callback_query_handler(lambda callback_query: callback_query.data=='how_to_start')
async def how_to_start(cq: CallbackQuery):
    msg = """
1️⃣Необходимо внести оплату 2490 сомов; наши реквизиты: 
Мбанк 0703666656
Элсом 0501619690
Optima (долларовый счет): 4169 5853 5847 4186

2️⃣Прикрепить чек сюда в сообщениях и отправить

Наши модераторы добавят вас в группу. 

‼️Внимание 
 1. Не надо ждать даты старта, у нас нет потоков или даты старта групп.
 2. Можно приступить к программе в любое удобное для вас время.
    """
    await bot.send_message(cq.message.chat.id, msg, reply_markup=kb.get_faq_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data=='about_program')
async def about_program(cq: CallbackQuery):
    msg = """
1️⃣Вы получаете детально расписанные технические задания проекта. Все технологии, которые заложены в проекте, утверждены компаниями. Все проекты составлены опытными middle разработчикам.✅

2️⃣Вы будете не одни, вас ждет наше дружелюбное сообщество. Нас уже более 60 junior разработчиков.

3️⃣Принимаете участие на мероприятиях с опытными разработчиками, в парных собеседованиях, обсуждаете проекты и учитесь друг у друга. Если у вас сложности, у вас будет у кого спросить.

4️⃣Программа полностью онлайн.
 
5️⃣Программа будет идти до вашего трудоустройства, и даже после. 
    """
    await bot.send_message(cq.message.chat.id, msg, reply_markup=kb.get_faq_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data=='when')
async def date_handler(cq: CallbackQuery):
    msg = """
Можете приступать прямо сейчас. 

‼️У нас нет понятия старта программы. Нет потоков. 

✅Желающие могут начать когда удобно.
    """
    await bot.send_message(cq.message.chat.id, msg, reply_markup=kb.get_faq_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data=='price')
async def price_handler(cq: CallbackQuery):
    msg = """
Стоимость участия $30 или 2490 сомов. 

✅Это единоразовый платеж, других обязательных оплат нет.
✅Также, нет ежемесячной платы за подписку.
    """
    await bot.send_message(cq.message.chat.id, msg, reply_markup=kb.get_faq_keyboard())




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)