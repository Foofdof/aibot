import io
import sqlite3
from collections import defaultdict

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, BufferedInputFile
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, Italic
)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta, datetime
from dbmanager import DBManager
from keyboards import menu_kb, statistics_kb, period_choose
from states import StatisticsSq

router = Router(name=__name__)


@router.message(F.text.lower() == "статистика")
async def statistics(message: Message, state: FSMContext):
    await state.set_state(StatisticsSq.statistics_chosen)
    await message.answer(
        "Выберите период",
        reply_markup=period_choose()
    )


@router.message(StatisticsSq.statistics_chosen, F.text)
async def choose_period(message: Message, state: FSMContext):
    await state.set_state(StatisticsSq.period_chosen)
    await state.update_data(period_chosen=message.text)

    data_stat = await state.get_data()
    per_dict = {
        "За день": (message.date - timedelta(days=1), message.date),
        "За неделю": (message.date - timedelta(weeks=7), message.date),
        "За месяц": (message.date - timedelta(days=30), message.date),
        "За все время": (datetime(1, 1, 1, 1, 1, 1), message.date)
    }
    period = per_dict[data_stat["period_chosen"]]

    user_id = message.from_user.id

    db = DBManager(connection=sqlite3.connect('finance.db'))
    data_db = db.select("operations", id=(user_id,), date=period)
    db.close()

    await state.set_state(StatisticsSq.data)
    await state.update_data({"data": data_db})

    await message.answer(
        "Отлично",
        reply_markup=statistics_kb()
    )


@router.message(StatisticsSq.data, F.text.lower() == "график по времени")
async def get_stat_plot_by_time(message: Message, state: FSMContext):
    data_stat = await state.get_data()
    await state.clear()
    data = data_stat["data"]
    period = data_stat["period_chosen"]

    income_dict = defaultdict(float)
    expense_dict = defaultdict(float)

    for record in data:
        date = mdates.datestr2num(record[0][:10])
        if record[1] > 0:
            income_dict[date] += record[1]
        else:
            expense_dict[date] -= record[1]

    dates_in, incomes = zip(*sorted(income_dict.items()))
    dates_exp, expenses = zip(*sorted(expense_dict.items()))

    fig, ax = plt.subplots()
    plt.grid(color='gray')

    ax.bar(dates_in, incomes, width=0.8, color='blue', label="Поступления")
    ax.bar(dates_exp, expenses, width=0.8, color='red', label="Расходы")
    ax.xaxis_date()
    fig.autofmt_xdate()
    ax.set_xlabel('Дата')
    ax.set_ylabel('Сумма операции')

    plt.title(f'Операции по датам {period.lower()}')
    plt.legend()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    await message.answer_photo(
        BufferedInputFile(
            buf.read(),
            filename="plot.png"
        ),
        caption="Изображение из буфера",
        show_caption_above_media=True,
        reply_markup=menu_kb()
    )


@router.message(StatisticsSq.data, F.text.lower() == "статистические параметры")
async def get_stat_indicators(message: Message, state: FSMContext):
    data_stat = await state.get_data()
    await state.clear()
    data = data_stat["data"]

    income = 0
    expenses = 0
    for record in data:
        if record[1] > 0:
            income += record[1]
        else:
            expenses += abs(record[1])

    content = as_list(
        as_marked_section(
            Bold(data_stat["period_chosen"] + ":   "),
            as_key_value(Italic('Поступления: '), income),
            as_key_value(Italic('Расходы: '), expenses),
            marker="    ",
        ),
        sep="\n\n",
    )

    await message.answer(
        **content.as_kwargs(),
        reply_markup=menu_kb()
    )
