from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🍽 В кафе", callback_data="dine_in")],
        [InlineKeyboardButton(text="🥡 С собой", callback_data="takeaway")],
        [InlineKeyboardButton(text="🛵 Доставка", callback_data="delivery")],
        [InlineKeyboardButton(text="📋 История заказов", callback_data="history")],
        [InlineKeyboardButton(text="ℹ️ О SANUKI", callback_data="about")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)