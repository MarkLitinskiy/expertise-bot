from aiogram import F
from aiogram import types

from bot import strings, crud
from bot import dispatcher

@dispatcher.callback_query(F.data == strings.cb_expert_statistics)
async def on_callback_statistics(cb: types.CallbackQuery):
    meetings = crud.read_all_examinations()
    examinations_data = []

    if not meetings:
        await cb.message.answer(text=strings.error_no_one_examination)
        return
    
    examinations_data.append(["Expert Name", "Expert TgID", "Client Name", "Client TgID", "Date", "Time", "Lat", "Lng", "House Info"])
    for meeting in meetings:
        examinations_data.append([
            str(meeting.expert.name),
            str(meeting.expert.telegram_id),
            str(meeting.client.name),
            str(meeting.client.telegram_id),
            str(meeting.date),
            f"{meeting.time.hour:02}:{meeting.time.minute:02}:{meeting.time.second:02}",
            str(meeting.lat),
            str(meeting.lng),
            str(meeting.house)
        ])
    
    data_str = '\n'.join([','.join(line) for line in examinations_data])
    data_file = types.BufferedInputFile(data_str.encode(), filename="examinations.csv")

    await cb.message.answer_document(data_file)