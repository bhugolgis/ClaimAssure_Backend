
from django.urls import path , re_path
from .views import *

urlpatterns = [
   
   #PreAuth Url's
    
    # path('PreAuthForm', PreAuthFormView.as_view(), name='PreAuthForm'),
    path('PersnolInfo', PersonalInfoPostAPI.as_view(), name='PersnolInfo Update API'),
    path('PersnolInfo/<str:id>', PersonalInfoUpdateAPI.as_view(), name='PersnolInfo Update API'),
    path('PreAuthDocumentUpdate/<str:preAuthID>', UpdatePreAuthDocumentView.as_view(), name='Update PreAuth Form'),
    path('ExistingPreAuthForm', ExistingnhmpIDPreAuthFormPost.as_view(), name='Existing PreAuth Form'),
    path('DeletePreAuth<str:preAuthID>', DeletePreAUth.as_view()),
    path('Download_zip_files/<str:preAuthID>/<str:choice>',DownloadPreAuthZipFile.as_view(), name='download PreAuth zip files'),
    path('LinkingcaseNumber',LinkingcaseNumberView.as_view(), name='Link caseNumber'),
    

    #Search Filters Url's
    re_path(r'SearchbynhmpID/(?P<nhmpID>.+)$', FilterbynhmpID.as_view(), name='Search by nhmpID'), 
    re_path(r'^SearchbypreAuthID/(?P<preAuthID>.+)$', SearchFilterbypreAuthID.as_view(), name='Search by PreAuth-ID'),
    re_path(r'^SearchbycaseNumber/(?P<caseNumber>.+)$', SearchFilterbycaseNumber.as_view() , name = 'Search by caseNumber'),

    path('EnhancementPost',PreAuthEnhancementPostAPI.as_view(), name='PreAuth Enhancement POST'),
    path('Enhancementget/<str:preAuthID>',PreAuthEnhancementGetAPi.as_view(), name='PreAuth Enhancement GET'),
    

]