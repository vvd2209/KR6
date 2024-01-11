from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Mailing


def do_mailing():
    mailing_objects = Mailing.objects.all()
    for mailing_object in mailing_objects:
        start_time_of_mailing_object = mailing_object.start_time
        end_time_of_mailing_object = mailing_object.end_time
        datetime_now = datetime.now()
        if datetime_now > start_time_of_mailing_object and datetime_now < end_time_of_mailing_object:
            all_client_objects = mailing_object.clients
            clients_email_list = [client.email for client in all_client_objects]
            send_mail(
                subject='Рассылка',
                message='Текст рассылки',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=clients_email_list
            )

