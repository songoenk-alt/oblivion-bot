# handlers/admin.py

import asyncio
import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from database import get_users_count, get_all_user_ids, export_users_txt
from keyboards import get_broadcast_confirm_keyboard

router = Router()

# Временное хранение сообщения для рассылки
pending_broadcast = {}

@router.message(F.text == "/admin_panel")
async def cmd_admin_panel(message: Message):
    """Секретная панель управления"""
    count = get_users_count()
    await message.answer(
        f"📊 <b>АДМИН ПАНЕЛЬ OBLIVION</b>\n\n"
        f"👥 Всего пользователей в базе: <b>{count}</b>",
        parse_mode="HTML"
    )

@router.message(F.text == "/admin_users")
async def cmd_admin_users(message: Message):
    """Выгрузка файла с базой данных"""
    await message.answer("⏳ Формирую список пользователей...")
    file_path = export_users_txt()
    
    document = FSInputFile(file_path)
    await message.answer_document(
        document=document,
        caption="📄 <b>База пользователей бота OBLIVION</b>",
        parse_mode="HTML"
    )
    if os.path.exists(file_path):
        os.remove(file_path)

@router.message(F.text.startswith("/admin_rassilka"))
async def cmd_admin_rassilka(message: Message):
    """Команда рассылки с поддержкой текста и фото"""
    # Отрезаем саму команду из текста
    raw_text = message.text[15:].strip() if len(message.text) > 15 else ""
    
    if not raw_text and not message.photo:
        await message.answer(
            "⚠️ <b>Как использовать рассылку:</b>\n"
            "Напишите: <code>/admin_rassilka Ваш текст рассылки</code>\n"
            "<i>(Или отправьте фото с такой подписью)</i>",
            parse_mode="HTML"
        )
        return

    # Сохраняем данные для рассылки
    pending_broadcast[message.from_user.id] = {
        "text": raw_text,
        "photo": message.photo[-1].file_id if message.photo else None
    }

    await message.answer("<b>📢 ПРЕДПРОСМОТР РАССЫЛКИ:</b>", parse_mode="HTML")
    
    if message.photo:
        await message.answer_photo(
            photo=message.photo[-1].file_id,
            caption=raw_text,
            reply_markup=get_broadcast_confirm_keyboard()
        )
    else:
        await message.answer(
            raw_text,
            reply_markup=get_broadcast_confirm_keyboard()
        )

@router.callback_query(F.data == "confirm_broadcast")
async def process_confirm_broadcast(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = pending_broadcast.get(user_id)
    
    if not data:
        await callback.answer("⚠️ Данные рассылки не найдены или устарели.", show_alert=True)
        return

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("🚀 Рассылка запущена...")

    user_ids = get_all_user_ids()
    success_count = 0
    fail_count = 0

    for u_id in user_ids:
        try:
            if data["photo"]:
                await callback.bot.send_photo(chat_id=u_id, photo=data["photo"], caption=data["text"])
            else:
                await callback.bot.send_message(chat_id=u_id, text=data["text"])
            success_count += 1
            await asyncio.sleep(0.05)  # Защита от лимитов Telegram
        except Exception:
            fail_count += 1

    del pending_broadcast[user_id]
    await callback.message.answer(
        f"✅ <b>Рассылка завершена!</b>\n\n"
        f"🟢 Успешно доставлено: <b>{success_count}</b>\n"
        f"🔴 Не доставлено (заблокировали бота): <b>{fail_count}</b>",
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "cancel_broadcast")
async def process_cancel_broadcast(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in pending_broadcast:
        del pending_broadcast[user_id]
    await callback.message.edit_text("❌ Рассылка отменена.")
    await callback.answer()