from aiogram.fsm.state import StatesGroup, State


class OperationSq(StatesGroup):
    operation_chosen = State()
    amount = State()
    description = State()
    remove_operation = State()


class StatisticsSq(StatesGroup):
    statistics_chosen = State()
    period_chosen = State()
    data = State()
