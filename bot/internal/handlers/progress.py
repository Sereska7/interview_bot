
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext


router = Router()

@router.message(F.text == "📊 Прогресс")
async def progress_section(message: types.Message):
    await message.answer(text="Окей")