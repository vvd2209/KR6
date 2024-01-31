from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from log.models import Log
from mailing.models import Mailing


# def do_mailing():
#     mailing_objects = Mailing.objects.all()
#     for mailing_object in mailing_objects:
#         start_time_of_mailing_object = mailing_object.start_time
#         end_time_of_mailing_object = mailing_object.end_time
#         datetime_now = datetime.now()
#         datetime_now = timezone.make_aware(datetime_now, timezone.get_current_timezone())
#         if datetime_now > start_time_of_mailing_object and datetime_now < end_time_of_mailing_object:
#             all_client_objects = mailing_object.clients
#             clients_email_list = [client.email for client in all_client_objects.all()]
#             send_mail(
#                 subject=mailing_object.message.title,
#                 message=mailing_object.message.text,
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=clients_email_list
#             )
            

def check_periodicity_mail_start(mail):
    """проверяет наступление условия отправки рассылки"""

    mail_start_time = mail.start_time
    mail_end_time = mail.end_time
    mail_day = mail.day
    mail_day_week = mail.day_week

    if mail_start_time > datetime.now().time() > mail_end_time:
        return True
    elif mail_day == datetime.now().day:
        return True
    elif mail_day_week == str(datetime.now().weekday()):
        return True
    else:
        return False


def mail_send(mail, client):
    """отправляет письма пользователям из рассылки по расписанию"""

    mail_send_ = send_mail(
        mail.title,
        mail.text,
        settings.EMAIL_HOST_USER,
        [client.email],
    )

    return mail_send_


def mail_status_chenge():
    """меняет статус рассылки 'запущена' на 'создана' после времени окончания рассылки"""
    mailing = Mailing.objects.filter(is_active=True)
    mailinglog = Log.objects.all()

    for mail in mailing:
        maillog = mailinglog.filter(mailing_current=mail).all().order_by('-time_try').first()
        if mail.status == 1 and mail.time_end.hour > datetime.now().hour:
            mail.status = 1
            mail.save()
        elif mail.status == 1 and maillog is not None and datetime.now().day > maillog.time_try.day():
            mail.status = 1
            mail.save()


