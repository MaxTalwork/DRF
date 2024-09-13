from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def email_update_course(email):
    send_mail(
        "Обновление курса",
        "Курс был обновлён!",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    