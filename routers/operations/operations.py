import sqlite3

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from dbmanager import DBManager
from keyboards import menu_kb, operations_kb
from states import OperationSq

router = Router(name=__name__)


@router.message(F.text.lower() == "операции")
async def operation(message: Message, state: FSMContext):
    await state.set_state(OperationSq.operation_chosen)
    await message.answer(
        "Добавить или удалить?",
        reply_markup=operations_kb()
    )


@router.message(F.text.lower() == "добавить", OperationSq.operation_chosen)
async def handle_add_operation(message: Message, state: FSMContext):
    await state.set_state(OperationSq.amount)
    await message.answer(
        "Введите сумму",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(OperationSq.amount, F.text)
async def add_operation(message: Message, state: FSMContext):
    amount = message.text
    await state.update_data(amount=amount)
    await state.set_state(OperationSq.description)
    await message.answer(
        "Отлично, введите описание"
    )


@router.message(OperationSq.description, F.text)
async def add_description(message: Message, state: FSMContext):
    description = message.text
    data = await state.update_data(description=description)
    await state.clear()

    user_id = message.from_user.id
    db = DBManager(connection=sqlite3.connect('finance.db'))

    table = {
        "name": "operations",
        "id": "INTEGER",
        "date": "TIMESTAMP",
        "operation": "REAL",
        "description": "TEXT"
    }
    db.create_table(table)
    db.insert("operations", user_id, message.date, data["amount"], data["description"])
    db.close()

    await message.answer(
        "Отлично, операция добавлена",
        reply_markup=menu_kb()
    )
