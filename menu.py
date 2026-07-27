from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db import user_exists, add_user
from keyboards import main_menu_keyboard

router = Router()

class Registration(StatesGroup):
    waiting_name = State()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user = user_exists(message.from_user.id)
    if user:
        await message.answer(
            f"С возвращением, <b>{user['name']}</b>! 👋\n\n"
            "Добро пожаловать в <b>SANUKI UDON SHOP</b>",
            reply_markup=main_menu_keyboard()
        )
        return

    await message.answer(
        "Добро пожаловать в <b>SANUKI UDON SHOP</b> 🍜\n\n"
        "Прежде чем начать, как к вам обращаться?"
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
        f"Спасибо, <b>{message.text}</b>! ✅\n\n"
        "Теперь можно сделать заказ:",
        reply_markup=main_menu_keyboard()
    )

# Команда /menu — вызывает главное меню в любой момент
@router.message(Command("menu"))
async def show_menu(message: Message):
    user = user_exists(message.from_user.id)
    if user:
        await message.answer("Главное меню:", reply_markup=main_menu_keyboard())
    else:
        await message.answer("Сначала пройдите регистрацию через /start")

# Обработчики нажатий на кнопки (пока заглушки)
@router.callback_query(F.data == "dine_in")
async def dine_in(callback: CallbackQuery):
    await callback.answer("Вы выбрали «В кафе»")
    await callback.message.answer("🛎 Скоро здесь будет оформление заказа в кафе.")

@router.callback_query(F.data == "takeaway")
async def takeaway(callback: CallbackQuery):
    await callback.answer("Вы выбрали «С собой»")
    await callback.message.answer("🥡 Скоро здесь будет оформление заказа с собой.")

@router.callback_query(F.data == "delivery")
async def delivery(callback: CallbackQuery):
    await callback.answer("Вы выбрали «Доставка»")
    await callback.message.answer("🛵 Скоро здесь будет оформление доставки.")

@router.callback_query(F.data == "history")
async def history(callback: CallbackQuery):
    await callback.answer("История заказов")
    await callback.message.answer("📋 Пока заказов нет. Сделайте первый!")

@router.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.answer("О нас")
    await callback.message.answer(
        "🍜 <b>SANUKI UDON SHOP</b>\n\n"
        "Мы готовим настоящий удон по японским рецептам.\n"
        "Ждём вас ежедневно с 11:00 до 23:00."
    )