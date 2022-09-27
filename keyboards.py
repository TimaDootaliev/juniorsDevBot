from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config


class Keyboard:
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