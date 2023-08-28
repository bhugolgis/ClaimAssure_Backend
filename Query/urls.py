from django.urls import path , re_path
from .views import *

urlpatterns = [

    path('GetPreAuthQueryList' , GetPreAuthQueryList.as_view() , name = 'GetPreAuthQueryList'),
    path('PostPreAuthQuery' , PostPreAuthQuery.as_view() , name = 'PostPreAuthQuery'),
    path('DownloadPreAuthQuery/<str:choice>/<int:id>' , DownloadPreAuthQueryDocument.as_view() , name = 'PostPreAuthQuery'),
    # re_path(r'^DownloadPreAuthQueryDocument/(?P<caseNumberID>.+)/(?P<choice>.+)$' , DownloadPreAuthQueryDocument.as_view() , name = 'PostPreAuthQuery'),
    path('GetClaimQueryList' , GetClaimQueryList.as_view() , name = 'GetClaimQueryList'),
    path('PostClaimQuery' , PostClaimQuery.as_view() , name = 'GetClaimQueryList'),
    path('DownloadClaimQueryDocument/<str:choice>/<int:id>' , DownloadClaimQueryDocument.as_view() , name = 'PostPreAuthQuery'),
    path('DeletePreAuthQuery/<int:id>' , DeletePreAuthQuery.as_view() , name = 'DeletePreAuthQuery'),
    # path('JSONFileView' , JSONFileView.as_view() , name = 'JSONFileView'),

]