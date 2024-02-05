import random

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from blogs.models import Blog
from client.forms import ClientForm
from client.models import Client
from mailing.models import Mailing


class MainPage(TemplateView):
    model = Blog
    template_name = 'client/main.html'
    extra_context = {
        'title': 'Сервис рассылки Your client'
    }
    context_object_name = 'objects_list'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings_count = len(Mailing.objects.all())
        mailings_is_active_count = len(Mailing.objects.filter(is_active=True))
        unique_clients_count = Client.objects.values('email').distinct().count()
        blog = Blog.objects.order_by('?')
        context['mailings_count'] = mailings_count
        context['mailings_is_active_count'] = mailings_is_active_count
        context['unique_clients_count'] = unique_clients_count
        context = {
            'blog': blog[:3],
            'mailings_count': mailings_count,
            'mailings_is_active_count': mailings_is_active_count,
            'unique_clients_count': unique_clients_count
        }
        return context


class ClientListView(PermissionRequiredMixin, ListView):
    model = Client
    template_name = 'client/client_list.html'
    context_object_name = 'objects_list'
    permission_required = 'client.view_client'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/client_detail.html'


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
    success_url = reverse_lazy('client:client_list')
    permission_required = 'client.add_client'

    def form_valid(self, form):
        new_client = form.save()
        if new_client.user is None:
            new_client.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('full_name', 'email', 'comment', 'user',)
    success_url = reverse_lazy('client:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')