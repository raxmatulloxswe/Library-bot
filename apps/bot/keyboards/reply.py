from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def reply_main_menu():
    reply_keyboard = ReplyKeyboardBuilder()

    reply_keyboard.button(text=_("Natija qo'shish➕"))
    reply_keyboard.button(text=_("Challanges🆚"))
    reply_keyboard.button(text=_("Kitoblar📚"))
    reply_keyboard.button(text=_("Sozlamalar⚙️"))

    reply_keyboard.adjust(2)

    return reply_keyboard.as_markup(resize_keyboard = True)

def reply_settings_menu():
    reply_keyboard = ReplyKeyboardBuilder()

    reply_keyboard.button(text=_("Ma'lumotlarimℹ️"))
    reply_keyboard.button(text=_("Tilni o'zgartirish🔄"))

    reply_keyboard.adjust(2)

    return reply_keyboard.as_markup(resize_keyboard = True)