from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.fsm.storage.memory import MemoryStorage

from . import config, strings

bot = Bot(token=config.token)

storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)

# Setup handlers
from . import register
from . import client_menu
from . import expert_menu

from .utils import calendar

# @dispatcher.message(Command('calendar'))
# async def on_cmd_calendar(msg: types.Message):
#     await msg.answer(text='Calendar', reply_markup=await calendar.Calendar.make_calendar())

# @dispatcher.callback_query(calendar.CalendarCallbackData.filter())
# async def on_callback_calendar(query: types.CallbackQuery):
#     data = calendar.CalendarCallbackData.unpack(query.data)
#     (datePicked, pickedDate) = await calendar.Calendar.process_selection(query, data)
#     if datePicked:
#         await query.answer(str(pickedDate))

@dispatcher.callback_query()
async def on_any_callback(cb: types.CallbackQuery):
    await cb.answer(strings.not_implemented)

async def start_bot():
    await dispatcher.start_polling(bot)