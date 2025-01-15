from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from apps.bot.models import Book, Comment
from apps.users.models import User
from apps.bot.utils.callback_data import PaginationCallbackData
from apps.bot.utils.states import BookListStatesGroup
from apps.bot.keyboards.inline import * # noqa

from asgiref.sync import sync_to_async

router = Router()


@router.message(F.text == __("Natija qo'shish➕"))
async def book_list(message: types.Message, state: FSMContext):

    await message.answer('Natija qo`shing!\n\n PS: 10-xx-200 oraliqda bo\'lgan bet sonini yozing!', reply_markup=ReplyKeyboardRemove())
