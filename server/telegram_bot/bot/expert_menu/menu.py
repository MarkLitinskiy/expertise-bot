from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot import strings

expert_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=strings.btn_my_examinations, callback_data=strings.cb_expert_examinations)],
    [InlineKeyboardButton(text=strings.btn_expert_statistics, callback_data=strings.cb_expert_statistics)],
])

async def send_menu_message(answerMsg: Message):
    await answerMsg.answer(
        text=strings.main_menu_message,
        reply_markup=expert_menu_keyboard
    )

async def edit_expert_menu(answerMsg: Message):
    await answerMsg.edit_text(
        text=strings.main_menu_message,
        reply_markup=expert_menu_keyboard
    )