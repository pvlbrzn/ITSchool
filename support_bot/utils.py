import os
from datetime import datetime

import pytz
import requests
from django.utils.html import escape
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TG_TOKEN')
CHAT_ID = os.getenv('TG_GROUP_CHAT_ID')


def send_telegram_message(text: str):
    """
    Send a message to a Telegram group via bot.

    Args:
        text (str): The message content, formatted in HTML.

    Returns:
        bool: True if message was sent successfully, False otherwise.
    """
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    response = requests.post(url, data=data)
    return response.status_code == 200

def notify_about_enrollment(request, enrollment):
    """
    Notify managers in Telegram about a new enrollment request.

    Args:
        request (HttpRequest): The current HTTP request object.
        enrollment (EnrollmentRequest): The enrollment instance.
    """
    site_url = request.build_absolute_uri('/')[:-1]
    manager_url = f'{site_url}/manager/manager/enrollments/'

    tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz)

    user_name = escape(enrollment.user.get_full_name())
    course_title = escape(enrollment.course.title)

    text = (
        f'📥 <b>Новая заявка:</b> № {enrollment.id}\n\n'
        f'👤 <b>Пользователь:</b> {user_name}\n'
        f'📚 <b>Курс:</b> {course_title}\n'
        f'🕒 <b>Дата:</b> {now.strftime("%d.%m.%Y %H:%M")}\n\n'
        f'➡️ <a href="{manager_url}">Перейти к заявкам</a>'
    )

    send_telegram_message(text)
