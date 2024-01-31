from django.contrib import admin

from mailing.models import Mailing, Message


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('get_clients', 'start_time', 'end_time', 'periodicity', 'status', 'message',)

    def get_clients(self, obj):
        if obj.clients.all():
            return list(obj.clients.all().values_list('email', flat=True))
        else:
            return 'NA'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text',)

