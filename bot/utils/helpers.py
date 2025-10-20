from aiogram.fsm.context import FSMContext


async def delete_old_messages(bot, chat_id: int, state: FSMContext):
    """Удаляем все сообщения, которые бот ранее отправил"""
    data = await state.get_data()
    sent_messages = data.get("sent_messages", [])

    for msg_id in sent_messages:
        try:
            await bot.delete_message(chat_id, msg_id)
        except Exception:
            pass

    await state.update_data(sent_messages=[])


async def save_message_id(state: FSMContext, message_id: int):
    """Сохраняем сообщение бота для последующего удаления"""
    data = await state.get_data()
    sent_messages = data.get("sent_messages", [])
    sent_messages.append(message_id)
    await state.update_data(sent_messages=sent_messages)
