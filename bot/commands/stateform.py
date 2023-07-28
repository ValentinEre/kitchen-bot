from aiogram.fsm.state import StatesGroup, State


class StateForm(StatesGroup):
    GET_BUTTON = State()
    GET_PRODUCT = State()
