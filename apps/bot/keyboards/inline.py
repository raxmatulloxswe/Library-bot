from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from apps.bot.utils.callback_data import * # noqa
from apps.bot.models import Comment


def inline_languages():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(text=_("O'zbek🇺🇿"), callback_data=cb_select_language_callback_data(lang=SelectLanguage.UZ))
    inline_keyboard.button(text=_("Rus🇷🇺"), callback_data=cb_select_language_callback_data(lang=SelectLanguage.RU))
    inline_keyboard.button(text=_("Ingliz🇺🇸"), callback_data=cb_select_language_callback_data(lang=SelectLanguage.EN))

    inline_keyboard.adjust(1)
    
    return inline_keyboard.as_markup()

def inline_books_pagination(pagination_data, page: int = 0):
    inline_keyboard = InlineKeyboardBuilder()

    start_offset = page * 5
    end_offset = min(start_offset + 5, len(pagination_data))

    for data in pagination_data[start_offset:end_offset]:
        inline_keyboard.row(InlineKeyboardButton(text=data.name, callback_data=PaginationCallbackData(name = str(data.id), page = page).pack()))

    buttons_row = []
    if page > 0:
        buttons_row.append(
            InlineKeyboardButton(text="⬅️", callback_data=PaginationCallbackData(name= "previous", page= page - 1).pack())
        )
    
    if end_offset < len(pagination_data):
        buttons_row.append(
            InlineKeyboardButton(text="➡️", callback_data= PaginationCallbackData(name= "next", page= page + 1).pack())
        )
    
    inline_keyboard.row(*buttons_row)
    
    return inline_keyboard.as_markup()


def inline_comment(book_id):
    inline_keyboard = InlineKeyboardBuilder()
    
    inline_keyboard.row(InlineKeyboardButton(text=_("Sharxlar💬"), callback_data=BookCommentCallbackData(name='comments', pk=book_id).pack()))
    inline_keyboard.row(InlineKeyboardButton(text=_("Sharx qoldirish"), callback_data=BookCommentCallbackData(name='add_comment', pk=book_id).pack()))
    
    return inline_keyboard.as_markup()

def inline_comments_pagination(pagination_data, page: int = 0):
    inline_keyboard = InlineKeyboardBuilder()
    
    start_offset = page * 1
    end_offset = min(start_offset + 1, len(pagination_data))
    
    buttons_row = []
    if page > 0:
        buttons_row.append(
            InlineKeyboardButton(text="⬅️", callback_data=PaginationCallbackData(name= "previous", page= page - 1).pack())
        )
    
    if end_offset < len(pagination_data):
        buttons_row.append(
            InlineKeyboardButton(text="➡️", callback_data= PaginationCallbackData(name= "next", page= page + 1).pack())
        )
    
    inline_keyboard.row(*buttons_row)
    
    return inline_keyboard.as_markup()

def inline_confirm():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.row(InlineKeyboardButton(text=_("Confirm✅"), callback_data=ConfirmCallbackData(name='confirm').pack()))
    inline_keyboard.row(InlineKeyboardButton(text=_("No🚫"), callback_data=ConfirmCallbackData(name='no').pack()))

    return inline_keyboard.as_markup()