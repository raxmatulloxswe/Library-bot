from aiogram.fsm.state import State, StatesGroup


class UpdateLanguageStatesGroup(StatesGroup):
    language = State()

class BookListStatesGroup(StatesGroup):
    books_list = State()
    book_detail = State()
    comments = State()
    add_comment = State()

class AddResultStatesGroup(StatesGroup):
    go_to_book = State()
    new_result = State()
    result_confirm = State()
