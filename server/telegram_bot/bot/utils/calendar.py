from typing import Tuple, Optional

import calendar
from datetime import datetime, timedelta

from bot import strings

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

class CalendarCallbackData(CallbackData, prefix='calendar'):
    userData: str
    action: str
    year: int
    month: int
    day: int

async def make_calendar(
    userData: str = "N",
    year: int = datetime.now().year,
    month: int = datetime.now().month,
    cancelBtnData: Optional[str] = None,
) -> InlineKeyboardMarkup:
    inline_kb_builder = InlineKeyboardBuilder()

    ignore_callback = CalendarCallbackData(action="ignore", userData=userData, year=year, month=month, day=0).pack()  # for buttons with no answer
    # First row - Month and Year
    kb_row = []
    kb_row.append(InlineKeyboardButton(
        text="<<",
        callback_data=CalendarCallbackData(action="prevYear", userData=userData, year=year, month=month, day=1).pack()
    ))
    kb_row.append(InlineKeyboardButton(
        text=f'{calendar.month_name[month]} {str(year)}',
        callback_data=ignore_callback
    ))
    kb_row.append(InlineKeyboardButton(
        text=">>",
        callback_data=CalendarCallbackData(action="nextYear", userData=userData, year=year, month=month, day=1).pack()
    ))
    inline_kb_builder.row(*kb_row)
    # Second row - Week Days
    kb_row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        kb_row.append(InlineKeyboardButton(text=day, callback_data=ignore_callback))
    inline_kb_builder.row(*kb_row)

    # Calendar rows - Days of month
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        kb_row = []
        for day in week:
            if (day == 0):
                kb_row.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
                continue
            kb_row.append(InlineKeyboardButton(
                text=str(day), callback_data=CalendarCallbackData(action="selectDay", userData=userData, year=year, month=month, day=day).pack()
            ))
        inline_kb_builder.row(*kb_row)

    # Last row - Buttons
    kb_row = []
    kb_row.append(InlineKeyboardButton(
        text="<", callback_data=CalendarCallbackData(action="prevMonth", userData=userData, year=year, month=month, day=day).pack()
    ))
    kb_row.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
    kb_row.append(InlineKeyboardButton(
        text=">", callback_data=CalendarCallbackData(action="nextMonth", userData=userData, year=year, month=month, day=day).pack()
    ))
    inline_kb_builder.row(*kb_row)

    if cancelBtnData is not None:
        inline_kb_builder.row(InlineKeyboardButton(text=strings.btn_cancel, callback_data=cancelBtnData))

    return inline_kb_builder.as_markup()

async def process_selection(
    query: CallbackQuery,
    data: CalendarCallbackData,
    cancelBtnData: Optional[str] = None
) -> Tuple[bool, datetime]:
    return_data = (False, None)
    temp_date = datetime(data.year, data.month, 1)
    # processing empty buttons, answering with no action
    if data.action == "ignore":
        await query.answer(cache_time=60)
    # user picked a day button, return date
    if data.action == "selectDay":
        return_data = True, datetime(int(data.year), int(data.month), int(data.day))
    # user navigates to previous year, editing message with new calendar
    if data.action == "prevYear":
        prev_date = datetime(int(data.year) - 1, int(data.month), 1)
        await query.message.edit_reply_markup(reply_markup=await make_calendar(data.userData, int(prev_date.year), int(prev_date.month), cancelBtnData))
    # user navigates to next year, editing message with new calendar
    if data.action == "nextYear":
        next_date = datetime(int(data.year) + 1, int(data.month), 1)
        await query.message.edit_reply_markup(reply_markup=await make_calendar(data.userData, int(next_date.year), int(next_date.month), cancelBtnData))
    # user navigates to previous month, editing message with new calendar
    if data.action == "prevMonth":
        prev_date = temp_date - timedelta(days=1)
        await query.message.edit_reply_markup(reply_markup=await make_calendar(data.userData, int(prev_date.year), int(prev_date.month), cancelBtnData))
    # user navigates to next month, editing message with new calendar
    if data.action == "nextMonth":
        next_date = temp_date + timedelta(days=31)
        await query.message.edit_reply_markup(reply_markup=await make_calendar(data.userData, int(next_date.year), int(next_date.month), cancelBtnData))
    # at some point user clicks DAY button, returning date
    return return_data
