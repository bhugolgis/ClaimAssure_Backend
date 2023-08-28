from django.urls import path , re_path
from .views import *

urlpatterns = [    


    path('CaseSheetPost', CaseSheetPostForm.as_view(), name='CaseSheetPost Claim Form'),
    re_path(r'^CaseSheetUpdate/(?P<caseNumber>.+)$', CaseSheetUpdateForm.as_view(), name='CaseSheetPost Claim Form'),

    path('LabtestPost', LabtestPostForm.as_view(), name='LabtestPost Claim Form'),
    re_path(r'^LabtestUpdate/(?P<caseNumber>.+)$', LabtestupdateForm.as_view(), name='LabtestPost Claim Form'),
    
    
    path('ReportsPost', ReportsPostForm.as_view(), name='ReportsPost Claim Form Post'),
    re_path(r'^ReportsUpdate/(?P<caseNumber>.+)$' , ReportsUpdateForm.as_view(), name='ReportsPost Claim Form Update'),

    path('DischargeSummaryPost', DischargesummuryPostAPI.as_view(), name='ReportsPost Claim Form'),
    re_path(r'^DischargeSummaryUpdate/(?P<caseNumber>.+)$' , DischargesummuryUpdateAPI.as_view(), name='ReportsPost Claim Form Update'),

    path('DeathSummaryPost', DeathSummuryPostAPI.as_view(), name='DeathSummury Claim Form'),
    re_path(r'^DeathSummaryUpdate/(?P<caseNumber>.+)$' ,  DeathSummuryUpdateAPI.as_view(), name='DeathSummury Claim Form'),
    
    path('BloodDocumentsPost', BloodDocumentsPostAPi.as_view(), name='Blood Documents Claim Form'),
    re_path(r'^BloodDocumentsUpdate/(?P<caseNumber>.+)$', BloodDocumentsUpdateApi.as_view(), name='Blood Documents Claim Form'),
    
    path('ClaimManagmentStatusPost', ClaimManagmentStatusPostAPI.as_view(), name='DeathSummury Claim Form'),
    path('GetClaimCountList', GetClaimCountList.as_view(), name='Get ClaimCount List'),

    path('MergeExcelFiles', ExcelMergexlsAPIView.as_view(), name='Merge Excel Files '),
    path('xls_ExcelUpload', DumpExcelInsertxls.as_view(), name='Excel Upload in database'),
    # path('xlsx_ExcelUpload', DumpExcelInsertxlsx.as_view(), name='Excel Upload in database'),
    path('MPClaimPiad_ExcelUpload', MPClaimPiadPostApi.as_view(), name='Excel Upload in database'),
    re_path(r'^DownloadClaimDocumnets/(?P<caseNumber>.+)/(?P<choice>.+)$', DownloadClaimDocuments.as_view(), name='Excel Upload in database'),

    path('DumpExcelView' , DumpExcelView.as_view(), name='Dump Excel View'),
    path('finalExcelView' , FinalExcel.as_view(), name='Dump Excel View'),


]