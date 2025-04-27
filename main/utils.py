from django.core.mail import send_mail


def send_welcome_email(to_email):
    send_mail(
        subject='Спасибо за подписку!',
        message='Вы успешно подписались на нашу рассылку!',
        from_email='blr.artyom.gonchar@gmail.com',
        recipient_list=[to_email],
        fail_silently=False,
    )
