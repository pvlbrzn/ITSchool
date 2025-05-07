import os
from datetime import datetime
import pytz
from dotenv import load_dotenv

from support_bot.bot import bot
from main.models import EnrollmentRequest


async def send_enrollment_to_group(bot, request, group_id: int, enrollment: EnrollmentRequest):
    site_url = request.build_absolute_uri('/')[:-1]
    manager_url = f'{site_url}/manager/manager/enrollments/'
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz)

    text = (
        f'📥 <b>Новая заявка:</b> № {enrollment.id}\n\n'
        f'👤 <b>Пользователь:</b> {enrollment.user.get_full_name()}\n'
        f'📚 <b>Курс:</b> {enrollment.course.title}\n'
        f'🕒 <b>Дата:</b> {now.strftime("%d.%m.%Y %H:%M")}\n\n'
        f'➡️ <a href="{manager_url}">Перейти к заявкам</a>'
    )
    await bot.send_message(chat_id=group_id, text=text)


async def send_enrollment_update(enrollment: EnrollmentRequest, request):
    load_dotenv()
    group_id = os.getenv('TG_GROUP_CHAT_ID')
    await send_enrollment_to_group(bot, request, group_id, enrollment)
    await bot.session.close()
