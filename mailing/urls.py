from django.urls import path
from client.apps import ClientConfig
from client.views import *
from mailing.apps import MailingConfig
from mailing.views import *

app_name = MailingConfig.name

urlpatterns = [
    path('mailings/', MailingListView.as_view(), name='mailing_list'),  # список рассылок
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),  # просмотр рассылки
    path('mailings/add/', MailingCreateView.as_view(), name='mailing_create'),  # создание рассылки
    path('mailings/edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),  # редактирование рассылки
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),  # удаление рассылки
]