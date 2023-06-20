from aiogram.dispatcher.filters.state import State, StatesGroup


class InitialState(StatesGroup):
    waiting_for_accept = State()
    waiting_for_settings = State()
    waiting_for_set_message_format = State()
