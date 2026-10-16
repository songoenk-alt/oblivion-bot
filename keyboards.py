# keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS

def get_subscription_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с каналами спонсоров"""
    buttons = []
    for ch in CHANNELS:
        buttons.append([InlineKeyboardButton(text=f"📢 {ch['title']}", url=ch['url'])])
    buttons.append([InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="check_subscription")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню бота"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Купить чит", callback_data="buy_cheat")],
            [InlineKeyboardButton(text="📜 Политика конфиденциальности", callback_data="privacy_policy")]
        ]
    )

def get_buy_keyboard() -> InlineKeyboardMarkup:
    """Кнопки под прайсом (разделенные Покупка и Поддержка)"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛒 Купить", url="https://t.me/ttsero"),
                InlineKeyboardButton(text="💬 Поддержка", url="https://t.me/ttsero")
            ],
            [InlineKeyboardButton(text="⭐ Отзывы", url="https://t.me/seroifixsensi")],
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_menu")]
        ]
    )

def get_back_keyboard() -> InlineKeyboardMarkup:
    """Кнопка возврата в меню"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_menu")]
        ]
    )

