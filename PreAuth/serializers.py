from rest_framework import serializers
from .models import *



class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ('nhmpID' , 'nameOfPatient' , 'adharPhotograph', 'adharNumber' ,
                  'dob' , 'gender' , 'mobileNumber' , 'alternativeNumber' ,  'addressLine1' ,
                   'addressLine2' , 'district' , 'pincode' , 'rationCardNumber' , 'rationCardPhotograph')

        def validate(self, data):
            if 'nhmpID' not in data or data['nhmpID'] == "":
                raise serializers.ValidationError('NHMP ID must be provided !!')
            if 'nameOfPatient' not in data or data['nameOfPatient'] == "":
                raise serializers.ValidationError('Name of Patient can not be empty !!')
            if 'adharNumber' not in data or data['adharNumber'] == "":
                raise serializers.ValidationError('Adhar Number field can not be empty !!')
            if 'dob' not in data or data['dob'] =="":
                raise serializers.ValidationError('DOB field can not be empty !!')
            
            return data


class PersonalInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        exclude = ('user', 'nhmpID')

class PreAuthDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreAuthDocument
        fields = '__all__'




class CombinedSerializer(serializers.Serializer):

    nhmpID = serializers.CharField(max_length=255, required=True)
    nameOfPatient = serializers.CharField(max_length=255, required=True)
    adharNumber = serializers.CharField(max_length=255, required=True)
    adharPhotograph = serializers.ImageField(required=  False)
    dob = serializers.DateField(required = True )
    gender = serializers.CharField(max_length=255, required=True)
    mobileNumber = serializers.IntegerField(required = True)
    alternativeNumber = serializers.IntegerField(required = False) 
    addressLine1 = serializers.CharField(max_length=255, required=False)
    addressLine2 = serializers.CharField(max_length=255, required=False)
    district = serializers.CharField(max_length=255, required=False)
    pincode = serializers.IntegerField(required= False)
    rationCardNumber = serializers.CharField(max_length=20, required=False)
    rationCardPhotograph =  serializers.ImageField(required= False)
    
    dateOfAdmission = serializers.DateTimeField(required = True)
    dateOfPreAuth = serializers.DateTimeField(required = True)
    hospitalName = serializers.CharField(max_length=255, required = True)
    hospitalCode = serializers.CharField(max_length=255 , required  = True)
    justification = serializers.ImageField(required = False)
    on_BedPhotograph = serializers.ImageField(required = False)
    admitCaseSheet = serializers.ImageField(required = False)
    labReport = serializers.ImageField(required = False)
    radiologyReport = serializers.FileField(required = False)

    
class ExistingPreAuthserializer(serializers.ModelSerializer):
    class Meta:
        model = PreAuthDocument
        fields = ('preAuthID','personalInfoID','dateOfAdmission' ,'dateOfPreAuth' , 'hospitalName' ,
                 'hospitalCode' , 'justification' , 'on_BedPhotograph' , 'admitCaseSheet', 'labReport', 'radiologyReport'  , 'claimAssure_status')



class ExistingPreAuthDocumentSerializer(serializers.Serializer):
    personalInfoID = serializers.CharField(required=True)
    dateOfAdmission = serializers.DateTimeField(required = True)
    dateOfPreAuth = serializers.DateTimeField(required = True)
    hospitalName = serializers.CharField(max_length=255, required = True)
    hospitalCode = serializers.CharField(max_length=255 , required  = True)
    justification = serializers.ImageField(required = False)
    on_BedPhotograph = serializers.ImageField(required = False)
    admitCaseSheet = serializers.ImageField(required = False)
    labReport = serializers.ImageField(required = False)
    radiologyReport = serializers.FileField(required = False)
    claimAssure_status = serializers.CharField(max_length=255 ,  required  = False)




class ZipFileSerializer(serializers.ModelSerializer):
    zip_file = serializers.FileField()

    class Meta:
        model = PreAuthDocument
        fileds = ( 'id', 'justification')


class caseNumberLinkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreAuthLinkcaseNumber
        fields = ('preAuthID' , 'caseNumber')

    # def create (self, validated_data):
    #     print("create")
    #     created = PreAuthLinkcaseNumber.objects.update_or_create(
    #         preAuthID=validated_data.get('preAuthID', None),
    #         caseNumber = validated_data.get('caseNumber' , None))
    #     return created.save()


class PreAuthSearchDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreAuthDocument
        fields = ( 'personalInfoID' , 'preAuthID' , 'dateOfAdmission',
                  'dateOfPreAuth' , 'hospitalName' , 'hospitalCode' , 'justification',
                  'on_BedPhotograph' , 'admitCaseSheet' , 'labReport' , 'radiologyReport' )



class PreAuthSearcViewhDocumentSerializer(serializers.ModelSerializer):
    caseNumber = serializers.SerializerMethodField()
    PMJY_status = serializers.SerializerMethodField()
    class Meta:
        model = PreAuthDocument
        fields = ( 'personalInfoID' , 'preAuthID' , 'caseNumber', 'claimAssure_status', 'PMJY_status',
                  'dateOfAdmission','dateOfPreAuth' , 'hospitalName' , 'hospitalCode' , 'justification',
                  'on_BedPhotograph' , 'admitCaseSheet' , 'labReport' , 'radiologyReport'   )
        
    def get_caseNumber(self, obj):
        try:
            case_numbers = obj.PreAuth_preAuthID.caseNumber
        except:
            case_numbers = ''
        return case_numbers
       
    def get_PMJY_status(self, obj):
        try:
            status = obj.PreAuth_preAuthID.MPClaimPaidExcel_caseNumber.get().workflowStatus
        except :
            status = ''
        return status


class PreAuthSearchDocumentUpdateSerializer(serializers.Serializer):
    dateOfAdmission = serializers.DateTimeField(required = False)
    dateOfPreAuth = serializers.DateTimeField(required = False)
    hospitalName = serializers.CharField(max_length=255, required = False)
    hospitalCode = serializers.CharField(max_length=255 , required  = False)
    justification = serializers.ImageField(required = False)
    on_BedPhotograph = serializers.ImageField(required = False)
    admitCaseSheet = serializers.ImageField(required = False)
    labReport = serializers.ImageField(required = False)
    radiologyReport = serializers.FileField(required = False)



class preauth_document_serializer_update_serializer(serializers.ModelSerializer):
    class Meta:
        model = PreAuthDocument
        fields = '__all__'
        # fields = ( 'dateOfAdmission','dateOfPreAuth' , 'hospitalName' , 'hospitalCode' , 'justification',
        #           'on_BedPhotograph' , 'admitCaseSheet' , 'labReport' , 'radiologyReport' )                


class PreAuthLinkcaseNumberSerialzier(serializers.ModelSerializer):
    class Meta:
        model = PreAuthLinkcaseNumber
        fields = '__all__'


class PreAuthEnhancementPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreAuthEnhancement
        fields = ('preAuthID' , 'query' , 'documents')
        
    def validate(self, data):
        if 'preAuthID' not in data or data['preAuthID'] == "":
            raise serializers.ValidationError('preAuthID can not be empty !!')
        if 'query' not in data or data['query'] == "":
            raise serializers.ValidationError('Query can not be empty !!')
    
        return data
        

class PreAuthEnhancementGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreAuthEnhancement
        fields = ('query' , 'documents')

import os
def delete_file(path):
    if os.path.exists(path):
        os.remove(path)



class PreAuthDocumnetDeleteSerializer(serializers.ModelSerializer):
    justification = serializers.FileField()
    on_BedPhotograph = serializers.FileField()
    admitCaseSheet = serializers.FileField()
    labReport = serializers.FileField()
    radiologyReport = serializers.FileField()


    class Meta:
        model = PreAuthDocument
        fields = ('justification', 'on_BedPhotograph' , 'admitCaseSheet' , 'labReport' , 'radiologyReport' )

    def delete(self, instance):
        delete_file(instance.justification.path)
        delete_file(instance.on_BedPhotograph.path)
        delete_file(instance.admitCaseSheet.path)
        delete_file(instance.labReport.path)
        delete_file(instance.radiologyReport.path)


class DownloadPreAuthZipFileSerializer(serializers.Serializer):
    choice = serializers.CharField(max_length=50 , required = True)


