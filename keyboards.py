from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Операции")
    kb.button(text="Статистика")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def operations_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить")
    kb.button(text="Удалить")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def statistics_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="График по времени")
    kb.button(text="Статистические параметры")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def period_choose() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="За день")
    kb.button(text="За неделю")
    kb.button(text="За месяц")
    kb.button(text="За все время")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)