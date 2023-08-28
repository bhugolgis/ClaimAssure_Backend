from django.urls import path , re_path
from .views import *

urlpatterns = [
   
   #PreAuth Url's
    
    # path('PreAuthForm', PreAuthFormView.as_view(), name='PreAuthForm'),
    path('DashboardAPI', DashboardAPI.as_view(), name='Dashboard API'), 


]