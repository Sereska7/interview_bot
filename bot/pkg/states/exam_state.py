from aiogram.fsm.state import StatesGroup, State

class ExamStates(StatesGroup):
    start = State()  # пользователь только зашёл в раздел
    in_process = State()  # сейчас просматривает вопрос
    showing_answer = State()