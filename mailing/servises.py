from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from log.models import Log
from mailing.models import Mailing


def check_start_mailing():
    mailing_objects = Mailing.objects.all()
    for mailing_object in mailing_objects:
        start_time_of_mailing_object = mailing_object.start_time
        end_time_of_mailing_object = mailing_object.end_time
        datetime_now = datetime.now()
        datetime_now = timezone.make_aware(datetime_now, timezone.get_current_timezone())
        if datetime_now > start_time_of_mailing_object and datetime_now < end_time_of_mailing_object:
            all_client_objects = mailing_object.clients
            clients_email_list = [client.email for client in all_client_objects.all()]
            send_mail(
                subject=mailing_object.message.title,
                message=mailing_object.message.text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=clients_email_list
            )


def mail_status_chenge():
    """меняет статус рассылки 'создана' на 'запущена' после времени окончания рассылки"""
    mailing = Mailing.objects.filter(is_active=True)
    mailinglog = Log.objects.all()

    for mail in mailing:
        maillog = mailinglog.filter(mailing_current=mail).all().order_by('-time_try').first()
        if mail.status == 'created' and mail.time_end.hour > datetime.now().hour:
            mail.status = 'created'
            mail.save()
        elif mail.status == 'created' and maillog is not None and datetime.now().day > maillog.time_try.day():
            mail.status = 'created'
            mail.save()


