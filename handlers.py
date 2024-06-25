from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards import get_yes_no_kb, menu_kb, operations_kb
from dbmanager import *
import datetime

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Что теперь?",
        reply_markup=menu_kb()
    )


@router.message(F.text.lower() == "операции")
async def operation(message: Message):
    await message.answer(
        "Добавить или удалить?",
        reply_markup=operations_kb()
    )


@router.message(F.text.lower() == "добавить")
async def add_op(message: Message):
    user_id = message.from_user.id
    db = DBManager(connection=sqlite3.connect('finance.db'))

    q = """
            CREATE TABLE IF NOT EXISTS operations (
            id INTEGER,
            date TIMESTAMP,
            operation REAL,
            description TEXT
            )
        """

    db.create_table(q)
    db.insert("operations", user_id, message.date, 300, "st")

    db.close()

    await message.answer(
        "Жаль...",
        reply_markup=ReplyKeyboardRemove()
    )
