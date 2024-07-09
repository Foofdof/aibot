from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from magic_filter import F

from keyboards import menu_kb

router = Router(name=__name__)


@router.message(Command("start"))
@router.message(Command("menu"))
@router.message(CommandStart(
    deep_link=True, magic=F.args == "start"
))
async def cmd_start(message: Message):
    await message.answer(
        "Что теперь?",
        reply_markup=menu_kb()
    )
