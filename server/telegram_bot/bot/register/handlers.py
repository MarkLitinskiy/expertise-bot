from aiogram import types, F
from aiogram.filters import CommandStart, state, StateFilter
from aiogram.fsm import state, context

from bot.client_menu import menu as client_menu
from bot.expert_menu import menu as expert_menu

from bot import dispatcher
from bot import strings, config, models, crud
from bot.database import session

class RegisterForm(state.StatesGroup):
    full_name = state.State()

    end = state.State()

@dispatcher.message(CommandStart(), StateFilter(None))
async def on_message_start(msg: types.Message, state: context.FSMContext):
    client = crud.get_client_by_tg(msg.from_user.id)
    if client is not None:
        if client.is_admin:
            await expert_menu.send_menu_message(msg)
        else:
            await client_menu.send_menu_message(msg)
    else:
        await state.set_state(RegisterForm.full_name)
        await msg.answer(strings.welcome_message)
        await msg.answer(strings.input_full_name)

@dispatcher.message(RegisterForm.full_name)
async def on_state_register_fullName(msg: types.Message, state: context.FSMContext):
    full_name = msg.text

    if len(full_name) < 2 or not full_name.isalpha():
        await state.set_state(RegisterForm.full_name)
        await msg.answer(strings.error_full_name)
        await msg.answer(strings.input_full_name)
    else:
        await state.update_data(full_name=full_name.strip())
        await on_register_end(msg, state)

async def on_register_end(msg: types.Message, state: context.FSMContext):
    ctx_data = await state.get_data()
    client = models.Clients(name=ctx_data["full_name"], telegram_id=msg.from_user.id, telegram_username=msg.from_user.username, is_admin=False)

    session.add(client)
    session.commit()

    await state.clear()
    await msg.answer(strings.registration_complete)
    await client_menu.send_menu_message(msg)

@dispatcher.message(F.text.startswith("/admin"))
async def on_message_admin(msg: types.Message):
    client = crud.get_client_by_tg(msg.from_user.id)
    if msg.text == f'/admin {config.admin_password}' and client is not None:
        session.query(models.Clients).filter(models.Clients.telegram_id==msg.from_user.id).update({
            models.Clients.is_admin: True
        })
        session.commit()

        await msg.answer(text=strings.admin_success)
    else:
        await msg.answer(text=strings.admin_failed)