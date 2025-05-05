from django.core.mail import send_mail
from django.urls import reverse


def send_welcome_email(to_email):
    send_mail(
        subject='Спасибо за подписку!',
        message='Вы успешно подписались на нашу рассылку!',
        from_email='blr.artyom.gonchar@gmail.com',
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_confirmation_email(subscriber, request):
    token = subscriber.confirmation_token
    confirm_url = request.build_absolute_uri(reverse('confirm_subscription', args=[token]))
    send_mail(
        subject='Подтверждение подписки',
        message=f'Здравствуйте! Подтвердите подписку по ссылке: {confirm_url}',
        from_email='blr.artyom.gonchar@gmail.com',
        recipient_list=[subscriber.email],
        fail_silently=False,
    )