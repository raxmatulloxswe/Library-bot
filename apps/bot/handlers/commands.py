from aiogram import Router, types, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from apps.bot.keyboards.reply import reply_main_menu


router = Router()

@router.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    await message.answer(_("Botga xush kelibsiz!"), reply_markup=reply_main_menu())


@router.message(Command('check_state'))
async def check_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer(f"State: {current_state}")


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish!"),
        BotCommand(command="check_state", description="Qaysi stateda ekanligini ko'rsatadi!"),
    ]
    await bot.set_my_commands(commands)