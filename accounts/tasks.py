import time

from celery import shared_task
from mail_templated import EmailMessage
from django.conf import settings


@shared_task
def send_email_task(obj):
    time.sleep(5)
    template_name = obj.pop('template_name')
    context = obj.pop('context')
    to = obj.pop('to')
    args = obj.pop('args')
    email_obj = EmailMessage(
        template_name,
        context,
        args,
        to=to,
    )
    email_obj.send()
