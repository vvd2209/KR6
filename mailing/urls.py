from django.urls import path
from client.apps import ClientConfig
from client.views import *
from mailing.apps import MailingConfig
from mailing.views import *

app_name = MailingConfig.name

urlpatterns = [
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/add/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/message_list/', MessageListView.as_view(), name='message_list'),
    path('mailings/message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('mailings/message_add/', MessageCreateView.as_view(), name='message_create'),
    path('mailings/message_edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('mailings/message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]