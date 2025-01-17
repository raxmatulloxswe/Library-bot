from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from apps.bot.models import Book, Results
from apps.bot.utils.states import AddResultStatesGroup
from apps.bot.keyboards.inline import * # noqa


router = Router()


@router.message(F.text == __("Natija qo'shish➕"))
async def add_result_func(message: types.Message, state: FSMContext):
    books = await sync_to_async(list)(Book.objects.all().only('id','name'))

    await message.answer('O\'qigan kitobingizni tanlang!\n\n<b>Faqat son kiriting!</b>', reply_markup=inline_books_pagination(books))
    await state.set_state(AddResultStatesGroup.go_to_book)


@router.callback_query(AddResultStatesGroup.go_to_book, PaginationCallbackData.filter())
async def go_to_book_for_result(callback_query: types.CallbackQuery, callback_data: PaginationCallbackData, state: FSMContext):
    if callback_data.name == 'next' or callback_data.name == 'previous':
        books = await sync_to_async(list)(Book.objects.all().select_related('author', 'category'))

        await callback_query.message.edit_reply_markup(
            reply_markup=inline_books_pagination(books, page=callback_data.page))
    else:
        book = await Book.objects.select_related('author', 'category').aget(id=callback_data.name)
        text = ("<b>Nomi: </b>{book_name}\n<b>Muallifi: </b>{book_author}\n<b>Kategoriya: </b>{book_category}\n\nNecha "
                "bet o'qiganingizni <b>faqat son</b>da kiriting!").format(
            book_name=book.name,
            book_author=book.author.name,
            book_category=book.category.name
        )

        await state.update_data({
            "book_name": book.name
        })
        await callback_query.message.answer(text, reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddResultStatesGroup.new_result)


@router.message(AddResultStatesGroup.new_result)
async def add_result_for_book(message: types.Message, state: FSMContext):
    try:
        num = int(message.text)
        if 10 <= num <= 200:
            state_data = await state.get_data()
            book_name = state_data['book_name']

            await message.answer(f"Siz o'qigan {num} bet eslab qolindi!")
            await Results.objects.acreate(
                user_id=message.from_user.id,
                book_name=book_name,
                read_pages_count=num)
            await state.set_state(AddResultStatesGroup.result_confirm)
        else:
            await message.answer('10 va 200 oralig\'ida o\'qishingiz kerak va shu oraliqda son kiriting!')
    except Exception as e:
        print(e)
        await message.answer("Boshidan urinib ko'ring!")

