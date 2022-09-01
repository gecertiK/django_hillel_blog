from celery import shared_task
from django.core.mail import send_mail as celery_send_mail


@shared_task
def send_mail_to_admin(text):
    celery_send_mail('Post', text, 'david@example.com', ['admin@example.com'])


@shared_task
def new_comment(message):
    celery_send_mail("Comment", message, 'admin@example.com', ['example@example.com'])
