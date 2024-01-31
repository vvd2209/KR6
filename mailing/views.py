from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.timezone import timedelta

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForms, MessageForms
from mailing.models import Mailing, Message


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    # def get_queryset(self):
    #     return super().get_queryset().filter(user=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    fields = ('start_time', 'end_time', 'periodicity', 'status', 'clients',)
    template_name = 'mailing/mailing_detail.html'


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForms
    permission_required = 'mailing.add_mailing'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.end_time = self.object.start_time + timedelta(minutes=5)
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForms
    permission_required = 'mailing.change_mailing'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = 'mailing.delete_mailing'
    success_url = reverse_lazy('mailing:mailing_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    fields = ('title', 'text',)
    template_name = 'mailing/message_detail.html'


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForms
    permission_required = 'mailing.add_message'
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForms
    permission_required = 'mailing.change_message'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    permission_required = 'mailing.delete_message'
    success_url = reverse_lazy('mailing:message_list')

