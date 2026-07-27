 from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from db import user_exists, add_user

router = Router()


class Registration(StatesGroup):
    waiting_name = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):

    user = user_exists(message.from_user.id)

    if user:

        await message.answer(
            f"🌸 С возвращением, <b>{user['name']}</b>!\n\n"
            "Добро пожаловать в <b>SANUKI UDON SHOP</b> 🍜"
        )

        return

    await message.answer(
        "🌸 Добро пожаловать в <b>SANUKI UDON SHOP</b>\n\n"
        "Прежде чем начать,\n"
        "как к вам обращаться?"
    )

    await state.set_state(Registration.waiting_name)


@router.message(Registration.waiting_name)
async def save_name(message: Message, state: FSMContext):

    add_user(
        telegram_id=message.from_user.id,
        name=message.text,
        username=message.from_user.username or ""
    )

    await state.clear()

    await message.answer(
        f"Спасибо, <b>{message.text}</b>! 🌸\n\n"
        "Теперь можно оформить заказ 🍜"
    )