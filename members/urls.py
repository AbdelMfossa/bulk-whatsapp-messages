from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy

app_name = 'members'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_url'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/', PasswordChangeView.as_view(success_url=reverse_lazy('members:logout')), name='change_password'),
]