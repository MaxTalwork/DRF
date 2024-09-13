from celery import shared_task
from datetime import datetime, timedelta

from users.models import User


@shared_task
def last_login_check():
    users = User.objects.filter(last_login=(datetime.now()-timedelta(days=31)))
    for user in users:
        user.is_active = False
