from aiogram import types, F
from aiogram.filters.callback_data import CallbackData

from bot import strings, crud
from bot import dispatcher

class MeetingCallbackData(CallbackData, prefix="expert_meeting"):
    meetingId: int

@dispatcher.callback_query(lambda cb: cb.data == strings.cb_expert_examinations)
async def on_callback_expertExaminations(cb: types.CallbackQuery):
    expert = crud.get_client_by_tg(cb.from_user.id)

    if expert is None or not expert.is_admin:
        await cb.message.answer(text=strings.error_unknown)
        return

    meetings = crud.read_expert_examinations(expert)

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
    MeetingCallbackData.filter()
)
async def on_callback_expertExaminationSelected(cb: types.CallbackQuery):
    meeting_data = MeetingCallbackData.unpack(cb.data)
    meeting = crud.get_meeting(meeting_data.meetingId)

    if meeting is None:
        await cb.message.answer(strings.error_unknown)
        return

    await cb.message.answer(text=strings.my_examination_full.format(
        meeting.client.name,
        str(meeting.date),
        meeting.time.hour,
        meeting.time.hour+1,
        meeting.house,
        strings.client_contact.format(meeting.client.telegram_username),
    ))
    await cb.message.answer_location(meeting.lat, meeting.lng)