import sqlite3

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)

from dbmanager import DBManager
from keyboards import menu_kb, statistics_kb
from states import MenuSq, StatisticsSq

router = Router(name=__name__)


@router.message(F.text.lower() == "статистика")
async def statistics(message: Message, state: FSMContext):
    await state.set_state(StatisticsSq.statistics_chosen)
    await message.answer(
        "Чего изволите?",
        reply_markup=statistics_kb()
    )


@router.message(StatisticsSq.statistics_chosen, F.text.lower() == "график по времени")
async def get_stat_plot_by_time(message: Message, state: FSMContext):
    await state.set_state(StatisticsSq.plot_by_time)

    await message.answer(
        "Вот",
        reply_markup=menu_kb()
    )


@router.message(StatisticsSq.statistics_chosen, F.text.lower() == "статистические параметры")
async def get_stat_indicators(message: Message, state: FSMContext):
    await state.clear()

    user_id = message.from_user.id

    db = DBManager(connection=sqlite3.connect('finance.db'))
    data = db.select("operations", user_id)
    db.close()

    total_income = 0
    total_expenses = 0
    for record in data:
        if record[1] > 0:
            total_income += record[1]
        else:
            total_expenses += abs(record[1])

    content = as_list(
        as_marked_section(
            Bold("Постуления за весь период:"),
            f"{total_income}",
            marker="",
        ),
        as_marked_section(
            Bold("Расходы за весь период:"),
            f"{total_expenses}",
            marker="",
        ),
        as_marked_section(
            Bold("За последний месяц:"),
            as_key_value("Поступления", 4),
            as_key_value("Расходы", 3),
            as_key_value("Остаток", total_income-total_expenses),
            marker="",
        ),
        sep="\n\n",
    )

    await message.answer(
        **content.as_kwargs(),
        reply_markup=menu_kb()
    )
