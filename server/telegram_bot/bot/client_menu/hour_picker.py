from aiogram import types
from aiogram.filters.callback_data import CallbackData

defaultFirstHour = 9
defaultLastHour = 18

class CbData(CallbackData, prefix='hourPicker'):
    hour: int

def make(first: int, last: int) -> types.InlineKeyboardMarkup:
    kb_buttons = []

    for hour in range(first, last):
        btn_text = f'{hour:02}:00'
        kb_buttons.append([types.InlineKeyboardButton(text=btn_text, callback_data=CbData(hour=hour).pack())])
    
    return types.InlineKeyboardMarkup(inline_keyboard=kb_buttons)
