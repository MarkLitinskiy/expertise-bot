from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.methods import SendMessage

from bot import strings

client_main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=strings.btn_register_examination, callback_data=strings.cb_register_examination)],
    [InlineKeyboardButton(text=strings.btn_move_examination, callback_data=strings.cb_move_examination)],
    [InlineKeyboardButton(text=strings.btn_cancel_examination, callback_data=strings.cb_cancel_examination)],
    [InlineKeyboardButton(text=strings.btn_my_examinations, callback_data=strings.cb_client_examinations)],
    [InlineKeyboardButton(text=strings.btn_operator_help, callback_data=strings.cb_operator_help)],
])

async def send_menu_message(answerMsg: types.Message):
    await answerMsg.answer(
        text=strings.main_menu_message,
        reply_markup=client_main_keyboard
    )

async def edit_menu_message(answerMsg: types.Message):
    await answerMsg.edit_text(
        text=strings.main_menu_message,
        reply_markup=client_main_keyboard
    )