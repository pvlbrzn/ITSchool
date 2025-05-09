from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpRequest

from main.models import Subscriber


def send_welcome_email(to_email: str) -> None:
    """
    Sends a welcome email to a newly subscribed user.

    :param to_email: Recipient's email address.
    """
    send_mail(
        subject='Спасибо за подписку!',
        message='Вы успешно подписались на нашу рассылку!',
        from_email='blr.artyom.gonchar@gmail.com',
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_confirmation_email(subscriber: Subscriber, request: HttpRequest) -> None:
    """
    Sends a confirmation email with a unique token link to verify the subscription.

    :param subscriber: Subscriber instance with a confirmation token.
    :param request: HttpRequest object to build the absolute confirmation URL.
    """
    token = subscriber.confirmation_token
    confirm_url = request.build_absolute_uri(reverse('confirm_subscription', args=[token]))
    send_mail(
        subject='Подтверждение подписки',
        message=f'Здравствуйте! Подтвердите подписку по ссылке: {confirm_url}',
        from_email='blr.artyom.gonchar@gmail.com',
        recipient_list=[subscriber.email],
        fail_silently=False,
    )
