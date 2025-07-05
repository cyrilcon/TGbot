from aiogram.fsm.state import State, StatesGroup


class Simple(StatesGroup):
    """Simple FSM"""

    simple_state = State()
