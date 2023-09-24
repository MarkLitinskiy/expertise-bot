import datetime

from aiogram import F
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot import crud, dispatcher, bot
from bot import strings, models
from bot.database import session

from bot.client_menu import hour_picker, menu

from bot.utils import calendar

class ExaminationStates(StatesGroup):
    pickDate = State()
    pickHour = State()
    pickLocation = State()
    pickHouse = State()

@dispatcher.callback_query(
    F.data == strings.cb_register_examination
)
async def on_callback_registerExamination(query: types.CallbackQuery, state: FSMContext):
    if await state.get_state() != None:
        await query.message.answer(text=strings.registration_canceled)
        await state.clear()
    await state.set_state(ExaminationStates.pickDate)
    await query.message.edit_text(text=strings.select_date_message, reply_markup=await calendar.make_calendar(userData=strings.cb_pick_examination_date, cancelBtnData=strings.cb_cancel_examination_creation))

@dispatcher.callback_query(
    StateFilter(ExaminationStates.pickDate),
    calendar.CalendarCallbackData.filter(F.userData == strings.cb_pick_examination_date)
)
async def on_callback_examinationCalendar(query: types.CallbackQuery, state: FSMContext):
    data = calendar.CalendarCallbackData.unpack(query.data)
    (isPicked, pickedDate) = await calendar.process_selection(query=query, data=data, cancelBtnData=strings.cb_cancel_examination_creation)
    if isPicked:
        today = datetime.datetime.today()
        if pickedDate < today:
            await query.answer(text=strings.error_date, show_alert=True)
            return

        await state.update_data(pickedDate=pickedDate)
        await state.set_state(ExaminationStates.pickHour)
        await edit_to_pickHour(query.message)

async def edit_to_pickHour(msg: types.Message):
    hoursKb = hour_picker.make(hour_picker.defaultFirstHour, hour_picker.defaultLastHour)
    hoursKb.inline_keyboard.append([types.InlineKeyboardButton(text=strings.btn_cancel, callback_data=strings.cb_cancel_examination_creation)])

    await msg.edit_text(
        text=strings.select_hour_message,
        reply_markup=hoursKb,
    )

@dispatcher.callback_query(
    StateFilter(ExaminationStates.pickHour),
    hour_picker.CbData.filter(),
)
async def on_callback_examinationHour(query: types.CallbackQuery, state: FSMContext):
    data = hour_picker.CbData.unpack(query.data)
    await state.set_state(ExaminationStates.pickLocation)
    await state.update_data(pickedHour=data.hour)
    await query.message.edit_text(strings.input_location)

@dispatcher.message(StateFilter(ExaminationStates.pickLocation))
async def on_message_location(msg: types.Message, state: FSMContext):
    if msg.location is None:
        await msg.answer(text=strings.error_no_location)
        await msg.answer(text=strings.input_location)
    else:
        await state.update_data(lat=msg.location.latitude, lng=msg.location.longitude)
        await state.set_state(ExaminationStates.pickHouse)
        await msg.answer(text=strings.input_house)

@dispatcher.message(StateFilter(ExaminationStates.pickHouse))
async def on_message_house(msg: types.Message, state: FSMContext):
    await msg.answer(strings.examination_register_wait_examinator)

    ctx_data = await state.get_data()
    pickedDate: datetime.date = ctx_data["pickedDate"].date()
    pickedHour: datetime.time = datetime.time(hour=ctx_data["pickedHour"])
    lat: float = ctx_data["lat"]
    lng: float = ctx_data["lng"]
    house = msg.text

    client = crud.get_client_by_tg(msg.from_user.id)
    expert = crud.find_examination_expert(lat, lng, client) if client is not None else None

    if client is None:
        await msg.answer(text=strings.error_examination_register)
    elif expert is None:
        await msg.answer(text=strings.error_no_such_expert)
    else:
        meeting = models.Meetings(expert=expert, client=client, date = pickedDate, time=pickedHour, lat=lat, lng=lng, house=house)
        session.add(meeting)

        if client.telegram_username != msg.from_user.username:
            client.telegram_username = msg.from_user.username
        
        session.commit()

        await bot.send_message(expert.telegram_id, text=strings.examination_register_complete_for_expert.format(str(pickedDate), pickedHour.hour, pickedHour.hour+1, f"@{client.telegram_username}"))
        await msg.answer(text=strings.examination_register_complete)

    await state.clear()

@dispatcher.callback_query(
    StateFilter(ExaminationStates.get_root()),
    F.data == strings.cb_cancel_examination_creation
)
async def on_callback_cancelExaminationCreation(cb: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await menu.edit_menu_message(cb.message)