from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from users.apps import UserConfig
from users.views import RegisterView, VerificationView, ErrorVerification, \
    UserProfileView, UserManagerListView, UserManagerProfileView

app_name = UserConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verification/', VerificationView.as_view(), name='verification'),
    path('verify_email/error/', ErrorVerification.as_view(), name='verify_email_error'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users_list/', UserManagerListView.as_view(), name='users_list'),
    path('profile_manager/<int:pk>/', UserManagerProfileView.as_view(), name='profile_manager'),
]