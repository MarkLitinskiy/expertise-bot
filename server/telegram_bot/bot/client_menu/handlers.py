from aiogram import types
from aiogram import F

from bot import dispatcher
from bot import strings

@dispatcher.callback_query(F.data == strings.cb_operator_help)
async def on_callback_operatorHelp(callback: types.CallbackQuery):
    await callback.message.answer(text=strings.operator_help_contact)