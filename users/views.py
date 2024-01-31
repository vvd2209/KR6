from random import random, randint

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserManagerForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verification')

    def form_valid(self, form):
        """ Форма отправки кода подтверждения почты пользователя """
        list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        if form.is_valid():
            verification_code = ''
            for i in range(8):
                rand_idx = randint(0, len(list)-1)
                verification_code += str(rand_idx)

            form.verification_code = verification_code
            user = form.save()
            user.verification_code = verification_code
            send_mail(
                subject='Поздравляем с регистрацией!',
                message=f'Подтвердите вашу регистрацию, введите код подтверждения {user.verification_code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            return super().form_valid(form)


class VerificationView(TemplateView):
    template_name = 'users/verification_email.html'

    def post(self, request):
        verification_code = request.POST.get('verification_code')
        user_code = User.objects.filter(verification_code=verification_code).first()

        if user_code.verification_code == verification_code:
            user_code.is_active = True
            user_code.save()
            return redirect('users:login')
        else:
            return redirect('users:verification_error')


class ErrorVerification(TemplateView):
    template_name = 'users/verification_email_error.html'
    success_url = reverse_lazy('users:verification_email')


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('client:main')

    def get_object(self, queryset=None):
        return self.request.user


class UserManagerProfileView(UpdateView):
    model = User
    form_class = UserManagerForm
    template_name = 'users/manager_profile.html'
    success_url = reverse_lazy('users:users_list')


class UserManagerListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'objects_list'
