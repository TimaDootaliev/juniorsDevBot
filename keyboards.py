from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:
    @classmethod
    def get_keyboard(cls):
        keyboard = InlineKeyboardMarkup(row_width=1).row(
            InlineKeyboardButton('Отправить чек', callback_data='send_check'),
            InlineKeyboardButton('FAQ', callback_data='faq')
        )
        return keyboard

    @classmethod
    def get_faq_keyboard(cls):
        keyboard = InlineKeyboardMarkup(row_width=1)
        buttons = (
            InlineKeyboardButton('Как начать?', callback_data='how_to_start'), 
            InlineKeyboardButton('Как проходит программа?', callback_data='about_programm'), 
            InlineKeyboardButton('Когда начнется?', callback_data='when'), 
            InlineKeyboardButton('Сколько стоит?', callback_data='price'), 
            InlineKeyboardButton(
                'Получить ссылку на видео', 
                callback_data='youtube', 
                url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley'
                )
        )
        for button in buttons:
            keyboard.add(button)
        return keyboard