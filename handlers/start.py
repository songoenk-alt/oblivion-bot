# handlers/start.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from config import CHANNELS
from keyboards import (
    get_main_menu_keyboard,
    get_buy_keyboard,
    get_back_keyboard
)

router = Router()

# Главный текст меню
MAIN_TEXT = (
    "<b>Welcome to OBLIVION</b>\n\n"
    "• Рабочий чит без рут прав и без бана.\n"
    "• Огромное количество реально полезных функций.\n"
    "• Лучший скинчейнджер на рынке модификаций с сохранением в облаке.\n\n"
    "📢 <b>Наш канал:</b> @serox_shop777"
)

# Красиво отформатированный прайс-лист
PRICE_TEXT = (
    "<b>💎 ПРАЙС-ЛИСТ НА МОДИФИКАЦИЮ OBLIVION</b>\n\n"
    "<b>⭐ Оплата в Звёздах (Telegram Stars):</b>\n"
    "├ 1 день — <b>50 ⭐️</b>\n"
    "├ 7 дней — <b>150 ⭐️</b>\n"
    "├ 30 дней — <b>300 ⭐️</b>\n"
    "├ 90 дней — <b>550 ⭐️</b>\n"
    "└ Навсегда — <b>800 ⭐️</b>\n"
    "<i>(Возможна оплата NFT)</i>\n\n"
    "<b>🪙 Оплата в Голде:</b>\n"
    "├ 1 день — <b>100 g</b>\n"
    "├ 7 дней — <b>350 g</b>\n"
    "├ 30 дней — <b>500 g</b>\n"
    "├ 60 дней — <b>800 g</b>\n"
    "└ Навсегда — <b>1200 g</b>\n\n"
    "<b>₽ Оплата в Рублях:</b>\n"
    "├ 1 день — <b>100 ₽</b>\n"
    "├ 7 дней — <b>300 ₽</b>\n"
    "├ 14 дней — <b>450 ₽</b>\n"
    "├ 30 дней — <b>650 ₽</b>\n"
    "├ 60 дней — <b>850 ₽</b>\n"
    "├ 90 дней — <b>1000 ₽</b>\n"
    "└ Навсегда — <b>1200 ₽</b>\n\n"
    "<b>💳 Способы оплаты:</b>\n"
    "Все популярные банки РФ и СНГ 🏦\n\n"
    "⭐️ <b>Отзывы:</b> <a href='https://t.me/seroifixsensi'>Нажмите сюда</a>\n"
    "🛒 <b>Покупка и поддержка:</b> @ttsero"
)

# Оформленная политика конфиденциальности
POLICY_TEXT = (
    "<b>📜 Ограничения и ответственность</b>\n"
    "<i>Редакция от 16 октября 2026 года</i>\n\n"
    "<b>1. Технические моменты</b>\n"
    "Магазин не несёт ответственности за сбои и неполадки, влияющие на доступность бота или обработку заказов, однако мы всегда стараемся минимизировать такие ситуации.\n\n"
    "<b>2. Изменения условий</b>\n"
    "Условия работы магазина могут обновляться без предварительного уведомления. Рекомендуем периодически знакомиться с актуальной редакцией правил.\n\n"
    "<b>3. Риски использования</b>\n"
    "Все операции совершаются под ответственность пользователя. Магазин не отвечает за убытки или проблемы, возникшие в результате использования полученной валюты / софта.\n\n"
    "<b>4. Антифрод-защита</b>\n"
    "При выявлении подозрительной активности заказ может быть приостановлен или отменён для предотвращения мошенничества.\n\n"
    "⚠️ <b>ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ И УСЛОВИЯ ВОЗВРАТА:</b>\n"
    "Возврат средств <b>НЕ ОСУЩЕСТВЛЯЕТСЯ</b> в следующих случаях:\n"
    "• В поддержку отправлены чужие/сторонние файлы и ключи, не сгенерированные нами.\n"
    "• Заявлено, что ключи недействительны, без доказательств со стороны покупателя.\n"
    "• На вашем устройстве имеются технические неполадки с софтом.\n"
    "• Товар вам просто не понравился или не оправдал ожиданий.\n"
    "• Ключ не подходит/не работает конкретно на вашем устройстве по вашей вине.\n\n"
    "<i>Желаем всем приятных и удачных покупок!</i>\n"
    "Мы придерживаемся прозрачных правил и уважаем права наших клиентов.\n"
    "💬 <b>Вопросы и поддержка:</b> @ttsero"
)

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    """Приветственное сообщение с главным меню"""
    await message.answer(
        MAIN_TEXT,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )

@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery):
    """Проверка подписки"""
    bot = callback.bot
    user_id = callback.from_user.id
    subscribed_statuses = {"creator", "administrator", "member"}
    
    is_all_subscribed = True
    try:
        for ch in CHANNELS:
            chat_member = await bot.get_chat_member(chat_id=ch["username"], user_id=user_id)
            if chat_member.status not in subscribed_statuses:
                is_all_subscribed = False
                break
    except Exception:
        is_all_subscribed = False

    if is_all_subscribed:
        await callback.answer("✅ Подписка подтверждена!", show_alert=False)
        try:
            await callback.message.delete()
        except Exception:
            pass
            
        await callback.message.answer(
            MAIN_TEXT,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    else:
        await callback.answer(
            "❌ Вы всё ещё не подписались на все каналы!",
            show_alert=True
        )

@router.callback_query(F.data == "buy_cheat")
async def process_buy_cheat(callback: CallbackQuery):
    """Раздел покупки читов"""
    await callback.message.edit_text(
        PRICE_TEXT,
        reply_markup=get_buy_keyboard(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    await callback.answer()

@router.callback_query(F.data == "privacy_policy")
async def process_privacy_policy(callback: CallbackQuery):
    """Раздел политики конфиденциальности"""
    await callback.message.edit_text(
        POLICY_TEXT,
        reply_markup=get_back_keyboard(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_menu")
async def process_back_to_menu(callback: CallbackQuery):
    """Возврат в главное меню"""
    await callback.message.edit_text(
        MAIN_TEXT,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    await callback.answer()