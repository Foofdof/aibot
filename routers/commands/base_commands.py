from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import menu_kb

router = Router(name=__name__)


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Что теперь?",
        reply_markup=menu_kb()
    )
