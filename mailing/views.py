import smtplib

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.core.management import call_command
from datetime import datetime
from django.shortcuts import redirect, render
from django.utils.timezone import timedelta

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from client.models import Client
from log.models import Log
from mailing.forms import MailingForms, MessageForms, MailingManagerUpdateForm, MailingUpdateForm
from mailing.models import Mailing, Message
from mailing.servises import mail_status_chenge


def mailing_start():
    return call_command('make_mailing')


scheduler = BackgroundScheduler()
scheduler.add_job(mailing_start, 'interval', seconds=600)
scheduler.add_job(mail_status_chenge, 'interval', seconds=3600)
scheduler.start()


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    fields = ('start_time', 'end_time', 'periodicity', 'status', 'clients',)
    template_name = 'mailing/mailing_detail.html'


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForms
    permission_required = 'mailing.add_mailing'
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/mailing_form.html'

    def get(self, request, **kwargs):
        form = self.form_class(self.request.user, request.POST)
        context = {'form': form}
        return render(request, 'mailing/mailing_form.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            clients = form.cleaned_data.get('clients')
            if not clients:
                form.add_error('clients', 'Выберите хотя бы одного клиента.')
            mailing = form.save(commit=False)
            mailing.user = self.request.user
            mailing.save()
            form.save_m2m()
            return redirect(self.success_url)

    def form_valid(self, form):
        tz = pytz.timezone('Europe/Moscow')
        clients = [client.email for client in Client.objects.filter(user=self.request.user)]
        new_mailing = form.save()

        if new_mailing.start_time <= datetime.now(tz):
            mail_subject = new_mailing.message.title if new_mailing.message is not None else 'Рассылка'
            message = new_mailing.message.text if new_mailing.message is not None else 'Вам назначена рассылка'
            try:
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, clients)
                log = Log.objects.create(time_try=datetime.now(tz), status='Успешно', server_response='200', mailing_current=new_mailing)
                log.save()
            except smtplib.SMTPDataError as err:
                log = Log.objects.create(time_try=datetime.now(tz), status='Ошибка', server_response=err, mailing_current=new_mailing)
                log.save()

            except smtplib.SMTPException as err:
                log = Log.objects.create(time_try=datetime.now(tz), status='Ошибка', server_response=err, mailing_current=new_mailing)
                log.save()

            except Exception as err:
                log = Log.objects.create(time_try=datetime.now(tz), status='Ошибка', server_response=err, mailing_current=new_mailing)
                log.save()

            new_mailing.status = 3
            if new_mailing.user is None:
                new_mailing.user = self.request.user
            new_mailing.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingUpdateForm
    template_name = 'mailing/mailing_form.html'
    permission_required = 'mailing.change_mailing'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        if self.request.user.groups.filter(name='manager').exists():
            return MailingManagerUpdateForm
        else:
            return MailingUpdateForm


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = 'mailing.delete_mailing'
    success_url = reverse_lazy('mailing:mailing_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    fields = ('title', 'text',)
    template_name = 'mailing/message_detail.html'


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForms
    template_name = 'mailing/message_form.html'
    permission_required = 'mailing.add_message'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        new_message = form.save()
        if new_message.user is None:
            new_message.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForms
    permission_required = 'mailing.change_message'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    permission_required = 'mailing.delete_message'
    success_url = reverse_lazy('mailing:message_list')

