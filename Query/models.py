from django.db import models
from ClaimManagement.models import MPClaimPaidExcel
from Authentications.models import User
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from rest_framework.response import Response
# Create your models here.





class PreAuthQuery(models.Model):
    user = models.ForeignKey(User , related_name = "User_PreAuthQuery" , on_delete = models.CASCADE)
    caseNumberId = models.ForeignKey(MPClaimPaidExcel , related_name = 'PreAuthQuery_caseNumber' ,  on_delete=models.CASCADE)
    query =      models.TextField(max_length=255 )
    documents =  models.FileField(upload_to= 'Query/PreAuth' , blank = True , null = True)
    # status = models.CharField(max_length= 50 , blank = True , null = True )
    date_modified = models.DateTimeField(auto_now_add=True)


   
class ClaimQuery(models.Model):
    user = models.ForeignKey(User , related_name = "User_ClaimQuery" , on_delete = models.CASCADE)
    caseNumberId = models.ForeignKey(MPClaimPaidExcel , related_name = 'ClaimQuery_caseNumber' ,  on_delete=models.CASCADE)
    query =      models.TextField(max_length=255 )
    documents =  models.FileField(upload_to= 'Query/Claim' , blank = True , null = True)
    # status = models.CharField(max_length=50 , blank = True , null = True )
    date_modified = models.DateTimeField(auto_now_add=True)
