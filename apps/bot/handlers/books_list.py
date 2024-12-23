from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from apps.bot.models import Book, Comment
from apps.users.models import User
from apps.bot.utils.callback_data import PaginationCallbackData
from apps.bot.utils.states import BookListStatesGroup
from apps.bot.keyboards.inline import * # noqa

from asgiref.sync import sync_to_async

router = Router()




@router.message(F.text == __("Kitoblar📚"))
async def book_list(message: types.Message, state: FSMContext):
    books = await sync_to_async(list)(Book.objects.all().select_related('author', 'category'))
     
    await message.answer(text="Kitoblar ro'yxati:", reply_markup=inline_books_pagination(books))
    await state.set_state(BookListStatesGroup.book_detail)


@router.callback_query(BookListStatesGroup.book_detail, PaginationCallbackData.filter())
async def book_detail(callback_query: types.CallbackQuery, callback_data: PaginationCallbackData, state: FSMContext):
    
    if callback_data.name == 'next' or callback_data.name == 'previous':
        books = await sync_to_async(list)(Book.objects.all().select_related('author', 'category'))

        await callback_query.message.edit_reply_markup(reply_markup=inline_books_pagination(books, page=callback_data.page))
   
    else:
        book = await Book.objects.select_related('author', 'category').aget(id = callback_data.name)
        text = "Kitob haqida ma'lumot:\n<b>Nomi: </b>{book_name}\n<b>Muallifi: </b>{book_author}\n<b>Kitob tarfi: </b>{book_description}\n<b>Kategoriya: </b>{book_category}".format(
            book_name = book.name,
            book_author = book.author.name,
            book_description = book.description,
            book_category = book.category.name,
        )
        
        await state.update_data({
            "book_id": book.id
        })

        await callback_query.message.answer(text, reply_markup=inline_comment(book.id))

    await callback_query.answer(cache_time=0)



@router.callback_query(BookListStatesGroup.book_detail, BookCommentCallbackData.filter())
async def book_detail_comment(callback_query: types.CallbackQuery, callback_data: BookCommentCallbackData, state: FSMContext):

    if callback_data.name == 'comments':
        book_comments = await sync_to_async(lambda: list(
            Comment.objects.select_related('book', 'user').filter(book_id=callback_data.pk)
        ))()

        if book_comments:
            book_comment = book_comments[0]
            comment_text = _("<b>Yuboruvchi:</b> {user}\n\n {comment}").format(user = book_comment.user.first_name, comment = book_comment.comment)
        else:
            comment_text = _("No comments available.🙁")

        await callback_query.message.answer(text=comment_text, reply_markup=inline_comments_pagination(book_comments))
        await state.set_state(BookListStatesGroup.comments)
    
    elif callback_data.name == 'add_comment':
        await callback_query.message.answer(_('Sharh qoldiring'))
        await state.set_state(BookListStatesGroup.add_comment)

    await callback_query.answer(cache_time=0)


@router.callback_query(BookListStatesGroup.comments, PaginationCallbackData.filter())
async def book_detail_comments_pagination(callback_query: types.CallbackQuery, callback_data: PaginationCallbackData, state: FSMContext):

    state_data = await state.get_data()
    book_id = state_data['book_id']

    if callback_data.name == 'next' or callback_data.name == 'previous':

        book_comments = await sync_to_async(lambda: list(
            Comment.objects.select_related('book', 'user').filter(book_id=book_id)
        ))()

        if book_comments:
            start_offset = callback_data.page 
            end_offset = min(start_offset + 1, len(book_comments))
            
            book_comment = book_comments[start_offset:end_offset][0]

            comment_text = _("<b>Yuboruvchi:</b> {user}\n\n {comment}").format(user = book_comment.user.first_name, comment = book_comment.comment)

        else:
            comment_text = _("No comments available.")
        
        await callback_query.message.edit_text(text=comment_text)
        await callback_query.message.edit_reply_markup(reply_markup=inline_comments_pagination(book_comments, page=callback_data.page))

    await callback_query.answer(cache_time=0)


@router.message(BookListStatesGroup.add_comment)
async def book_add_comment_message(message: types.Message, state: FSMContext):
    comment_text = message.text
    await state.update_data({'comment': comment_text})

    await message.answer(_("<b>Sizning sharhingiz\n\n</b>{comment}\n").format(comment = comment_text), reply_markup=inline_confirm())

@router.callback_query(BookListStatesGroup.add_comment, ConfirmCallbackData.filter())
async def book_add_comment_query(callback_query: types.CallbackQuery, callback_data: ConfirmCallbackData, state: FSMContext):
    state_data = await state.get_data()

    book_id = state_data['book_id']
    comment_text = state_data['comment']
    
    if callback_data.name == 'confirm':
        await Comment.objects.acreate(
            user_id = callback_query.from_user.id,
            book_id = book_id,
            comment = comment_text
        )
    
    elif callback_data.name == 'no':
        await callback_query.message.answer(_('Sharh qoldiring'))
        
    
    await callback_query.answer(cache_time=0)
        
