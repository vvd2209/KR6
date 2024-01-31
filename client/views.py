import random

from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from blogs.models import Blog
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
        mailings_is_active_count = len(Mailing.objects.filter(status=2))
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



class ClientsListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    fields = ('full_name', 'email', 'comment',)
    success_url = reverse_lazy('client:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('full_name', 'email', 'comment',)
    success_url = reverse_lazy('client:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')