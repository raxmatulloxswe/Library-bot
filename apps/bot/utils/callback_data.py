from enum import Enum
from aiogram.filters.callback_data import CallbackData


class SelectLanguage(str, Enum):
    UZ = 'uz'
    RU = 'ru'
    EN = 'en'

class SelectLanguageCallbackData(CallbackData, prefix="select_language"):
    language: SelectLanguage

def cb_select_language_callback_data(lang):
    return SelectLanguageCallbackData(language=lang.value).pack()

class PaginationCallbackData(CallbackData, prefix="pag"):
    name: str
    page: int

class BookCommentCallbackData(CallbackData, prefix="com"):
    name: str
    pk: int

class ConfirmCallbackData(CallbackData, prefix="conf"):
    name: str