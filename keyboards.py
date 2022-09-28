from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from decouple import config


class kb:
    @classmethod
    def get_keyboard(cls):
        keyboard = InlineKeyboardMarkup(row_width=1).row(
            InlineKeyboardButton('💵 Отправить чек', callback_data='send_check'),
            InlineKeyboardButton('❓ FAQ', callback_data='faq')
        )
        return keyboard

    @classmethod
    def get_faq_keyboard(cls):
        keyboard = InlineKeyboardMarkup(row_width=1)
        buttons = (
            InlineKeyboardButton('🟢 Как начать?', callback_data='how_to_start'), 
            InlineKeyboardButton('💡 Как проходит программа?', callback_data='about_program'), 
            InlineKeyboardButton('🕑 Когда начнется?', callback_data='when'), 
            InlineKeyboardButton('💰 Сколько стоит?', callback_data='price'), 
            InlineKeyboardButton(
                '🎞 Видео "Что такое JuniorsDev?"', 
                callback_data='youtube', 
                url=config('VIDEO_URL')
                )
        )
        for button in buttons:
            keyboard.add(button)
        return keyboard

    
    @classmethod
    def send_check_button(cls):
        button1 = KeyboardButton('💵 Отправить чек')
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True, 
            one_time_keyboard=False
            )
        keyboard.add(button1)
        return keyboard


    @classmethod
    def cancel_button(cls):
        button1 = KeyboardButton('Отмена операции')
        button2 = KeyboardButton('💵 Отправить чек')
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True, 
            one_time_keyboard=False
            )
        keyboard.add(button1)
        keyboard.add(button2)
        return keyboard