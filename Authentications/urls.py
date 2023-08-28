
from django.urls import path
from .views import *
from knox import views as knox_views
from . import views

urlpatterns = [
    path('register', UserRegister.as_view(), name='Register'),
    path('login', LoginView.as_view(), name='login'),
    path('ChangePassword', ChangePasswordView.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='knox_logout'),

]