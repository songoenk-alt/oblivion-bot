# middlewares/subscription.py

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from config import CHANNELS
from keyboards import get_subscription_keyboard

class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        bot = event.bot

        # Разрешаем кнопке проверки подписки проходить без блокировки
        if isinstance(event, CallbackQuery) and event.data == "check_subscription":
            return await handler(event, data)

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
            # Пользователь подписан — пускаем к обычному коду
            return await handler(event, data)
        else:
            # Не подписан или отписался — блокируем и требуем подписаться
            if isinstance(event, Message):
                await event.answer(
                    "❌ Вы не подписаны на каналы (или отписались)!\nДля использования бота подпишитесь:",
                    reply_markup=get_subscription_keyboard()
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "❌ Вы до сих пор не подписаны на все каналы!",
                    show_alert=True
                )
            return