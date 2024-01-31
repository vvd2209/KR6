from django.urls import path

from log.apps import LogConfig
from log.views import LogListView

app_name = LogConfig.name

urlpatterns = [
    path('log_list', LogListView.as_view(), name='log_list'),
]