from celery import shared_task

from django.core.mail import send_mail

from .models import Subscriber


@shared_task
def send_newsletter_to_all(subject, message):
    """
    Celery task to send a newsletter email to all confirmed subscribers.

    :param subject: Email subject line
    :param message: Email body content
    """
    print("Запуск рассылки...")
    emails = Subscriber.objects.values_list('email', flat=True)
    for email in emails:
        print(f"Отправка на: {email}")
        try:
            send_mail(subject, message, 'blr.artyom.gonchar@gmail.com', [email],
                      fail_silently=False, )
            print(f"Отправлено: {email}")
        except Exception as e:
            print(f"Ошибка при отправке на {email}: {str(e)}")
