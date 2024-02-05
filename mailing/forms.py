from django import forms
from mailing.models import Mailing, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForms(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('start_time', 'end_time', 'periodicity', 'clients', 'message',)


class MessageForms(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'text', )


class MailingManagerUpdateForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ['clients']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].disabled = True
        self.fields['status'].disabled = True
        self.fields['start_time'].disabled = True
        self.fields['end_time'].disabled = True
        self.fields['periodicity'].disabled = True
        self.fields['user'].disabled = True
