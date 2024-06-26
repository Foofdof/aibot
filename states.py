from aiogram.fsm.state import StatesGroup, State


class OperationSq(StatesGroup):
    operation_chosen = State()
    amount = State()
    description = State()

    remove_operation = State


class Statistics(StatesGroup):
    statistics_chosen = State()
