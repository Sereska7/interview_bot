from aiogram.fsm.state import StatesGroup, State

class TestStates(StatesGroup):
    select_topic = State()
    select_level = State()
    ready_to_start = State()
    in_progress = State()
    show_result = State()
