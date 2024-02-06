from django.shortcuts import render
from django.views.generic import ListView

from log.models import Log


class LogListView(ListView):
    model = Log
    template_name = 'log/log_list.html'
    context_object_name = 'objects_list'
