from aiogram.fsm.state import StatesGroup, State

class TestStates(StatesGroup):
    select_topic = State()
    ready_to_start = State()
    in_progress = State()
    show_result = State()
