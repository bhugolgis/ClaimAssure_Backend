from django.db import models
from django.core.exceptions import ValidationError
from Authentications.models import User
from django.utils.translation import gettext_lazy as _ 

# Create your models here.

def validate_length(value):
    an_integer = value
    a_string = str(an_integer)
    length = len(a_string)
    if length > 12:
        raise ValidationError(f'{value} is above 12 digits')
    if length < 12:
        raise ValidationError(f'{value} is less than 12 digits')

def validate_number(value):
    an_integer = value
    a_string = str(an_integer)
    length = len(a_string)
    if length > 10:
        raise ValidationError(f'{value}  is above 10 digits')
    if length < 10:
        raise ValidationError(f'{value}  is less than 10 digits')

   
class PersonalInfo(models.Model):
    user = models.ForeignKey( User , related_name= "user_profile" , on_delete= models.CASCADE)
    nhmpID = models.CharField(max_length=255, unique= True  , primary_key= True )
    nameOfPatient = models.CharField(max_length= 255 , blank = True , null = True)
    adharPhotograph = models.ImageField(upload_to= 'AdharCard_PhotoGraphs' , blank = True , null = True )
    adharNumber = models.PositiveBigIntegerField(validators=[validate_length] , blank = True , null = True , unique= True)
    dob = models.DateField( blank = True , null = True )
    gender = models.CharField(max_length=15 , blank = True , null = True )
    mobileNumber = models.PositiveBigIntegerField( validators=[validate_number] , blank = True , null = True)
    alternativeNumber =  models.PositiveBigIntegerField(validators=[validate_number] , blank = True , null = True)
    addressLine1 = models.CharField(max_length= 255 , blank = True , null = True )
    addressLine2 = models.CharField(max_length=  255 , blank= True , null = True)
    district = models.CharField(max_length = 50 , blank = True , null = True)
    pincode = models.IntegerField(blank = True , null = True )
    rationCardNumber = models.CharField(max_length=50 ,  blank = True , null = True )
    rationCardPhotograph = models.ImageField( upload_to= 'RationCard_Photographs'  , blank = True , null = True)

    def __str__(self):
        return self.nhmpID

class PreAuthDocument(models.Model):
    user = models.ForeignKey(User , related_name= "Preauth_document" , on_delete=models.CASCADE)
    personalInfoID = models.ForeignKey(PersonalInfo , related_name="PreAuth_personal" ,  to_field='nhmpID' , db_column= 'personalInfo' ,on_delete=models.CASCADE)
    preAuthID = models.CharField(max_length=255 ,unique=True , primary_key= True )
    dateOfAdmission = models.DateTimeField( null = True )
    dateOfPreAuth = models.DateTimeField( null = True )
    hospitalName = models.CharField(max_length= 255 , blank = False , null = True)
    hospitalCode = models.CharField(max_length= 255 , blank = False , null = True)
    justification = models.FileField(upload_to='PreAuthDocuments/justification' , blank = True , null = True )
    on_BedPhotograph = models.FileField(upload_to= 'PreAuthDocuments/on_bedPhotograph' , blank = True ,     null = True )   
    admitCaseSheet = models.FileField(upload_to= 'PreAuthDocuments/admitCaseSheet' ,  blank = True , null = True )
    labReport = models.FileField(upload_to= 'PreAuthDocuments/labReport' , blank = True , null = True)
    radiologyReport = models.FileField(upload_to= 'PreAuthDocuments/radiologyReport' , blank = True , null = True)
    claimAssure_status = models.CharField(max_length= 100  ,default= 'PreAuth Created', blank = True , null = True )

    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.preAuthID

class PreAuthLinkcaseNumber(models.Model):
    user = models.ForeignKey(User ,  related_name= "PreAuthLinkcaseNumber_user" ,on_delete= models.CASCADE)
    preAuthID = models.OneToOneField(PreAuthDocument , related_name= "PreAuth_preAuthID" , to_field= 'preAuthID',  on_delete=models.SET_NULL , blank= True , null = True  )
    caseNumber = models.CharField(max_length=100 , unique= True  , primary_key= True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.caseNumber


class PreAuthEnhancement(models.Model):
    user = models.ForeignKey(User , related_name = 'PreAuthEnhancement_User' , on_delete = models.CASCADE)
    preAuthID = models.ForeignKey(PreAuthDocument , related_name = 'PreAuthEnhancement_PreAuthDocument' ,  to_field= 'preAuthID' , on_delete = models.CASCADE)
    query = models.CharField(max_length = 255 , blank = True , null = True)
    documents = models.FileField(upload_to = 'PreAuthDocuments/Enhancement_Documents' , blank = True , null = True)


# class PreAuthQuery(models.Model):
#     caseNumber = models.ForeignKey(PreAuthLinkcaseNumber , related_name='preAuthQuery_caseNumber',  to_field= 'caseNumber' ,  on_delete=models.CASCADE )
#     query = models.TextField(max_length=255 , blank = True , null = True)
#     documents = models.FileField(upload_to= 'Query/PreAuth_Query', blank = True , null = True)