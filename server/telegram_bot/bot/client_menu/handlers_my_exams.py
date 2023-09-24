from aiogram import types, F
from aiogram.filters.callback_data import CallbackData

from bot import crud

from bot import dispatcher
from bot import strings

class MeetingCallbackData(CallbackData, prefix="client_meeting"):
    meetingId: int

@dispatcher.callback_query(F.data == strings.cb_client_examinations)
async def on_callback_clientExaminations(cb: types.CallbackQuery):
    client = crud.get_client_by_tg(cb.from_user.id)

    if client is None:
        await cb.message.answer(text=strings.error_unknown)
        return

    meetings = crud.read_client_examinations(client)

    if not meetings:
        await cb.message.answer(text=strings.error_no_one_examination)
    else:
        kb_buttons = []

        for meeting in meetings:
            meetingDate = str(meeting.date)
            meetingHour = meeting.time.hour

            kb_buttons.append([types.InlineKeyboardButton(
                text=strings.my_examination_btn_data.format(meetingDate, meetingHour),
                callback_data=MeetingCallbackData(meetingId=meeting.id).pack()
            )])

        await cb.message.answer(text=strings.my_examinations_message, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb_buttons))

@dispatcher.callback_query(
    MeetingCallbackData.filter(),
)
async def on_callback_clientExaminationSelected(cb: types.CallbackQuery):
    meeting_data = MeetingCallbackData.unpack(cb.data)
    meeting = crud.get_meeting(meeting_data.meetingId)

    if meeting is None:
        await cb.message.answer(text=strings.error_unknown)
        return

    await cb.message.answer(text=strings.my_examination_full.format(
        meeting.client.name,
        str(meeting.date),
        meeting.time.hour,
        meeting.time.hour+1,
        meeting.house,
        str()
    ))
    await cb.message.answer_location(meeting.lat, meeting.lng)