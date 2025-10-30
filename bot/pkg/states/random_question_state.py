from aiogram.fsm.state import StatesGroup, State

class RQStates(StatesGroup):
    in_progress = State()