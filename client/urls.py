from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig
from client.views import *

app_name = ClientConfig.name

urlpatterns = [
    path('', cache_page(60)(MainPage.as_view()), name='main'),  # главная страница
    path('clients/', ClientsListView.as_view(), name='client_list'),  # список клиентов
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),  # просмотр клиента
    path('clients/add/', ClientCreateView.as_view(), name='client_create'),  # создание клиента
    path('clients/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),  # редактирование клиента
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),  # удаление клиента
]
