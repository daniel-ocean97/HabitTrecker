# habits/tasks.py
import logging

import telegram
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Habit

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminders():
    now = timezone.localtime(timezone.now())
    current_time = now.time().replace(second=0, microsecond=0)
    current_weekday = now.weekday() + 1  # Monday=1, Sunday=7

    habits = Habit.objects.filter(time=current_time).select_related("user")

    if not habits:
        return

    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

    for habit in habits:
        if not habit.user.telegram_chat_id:
            continue
        if should_remind_today(habit, current_weekday):
            try:
                message = (
                    f"⏰ Напоминание о привычке:\n"
                    f"• Действие: {habit.action}\n"
                    f"• Место: {habit.place}\n"
                    f"• Время на выполнение: {habit.duration} секунд\n"
                    f"• Запланировано на: {habit.time.strftime('%H:%M')}"
                )
                bot.send_message(chat_id=habit.user.telegram_chat_id, text=message)
                logger.info(f"Sent reminder to {habit.user} for habit {habit.id}")
            except telegram.error.TelegramError as e:
                logger.error(f"Telegram error for user {habit.user.id}: {e}")
            except Exception as e:
                logger.exception(f"Error sending reminder: {e}")


def should_remind_today(habit, current_weekday):
    """Проверяет, нужно ли напоминать сегодня"""
    # Для ежедневных привычек
    if habit.periodicity == 1:
        return True

    # Для привычек с определенной периодичностью
    days_since_creation = (timezone.now() - habit.created_at).days
    return days_since_creation % habit.periodicity == 0
