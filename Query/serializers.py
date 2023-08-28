from rest_framework import serializers
from ClaimManagement.models import *
from .models import PreAuthQuery , ClaimQuery

class GetPreAuthQueryListSerializer(serializers.ModelSerializer):
    preAuthId = serializers.SerializerMethodField()
    dateOfPreAuth = serializers.SerializerMethodField()
    hospitalCode = serializers.SerializerMethodField()
    class Meta:
        model = MPClaimPaidExcel
        fields = ('id' ,'preAuthId' , 'caseNumber' , 'dateOfPreAuth', 'hospitalName' , 'hospitalCode' ,'admissionDate',
                   'preauthPendingRemarks' , 'preAuthQueryStatus')

    def get_preAuthId(self, obj):
        try:
            preAuthId = obj.caseNumber.preAuthID.preAuthID
        except:
            preAuthId = ''
            
        return preAuthId
    
    def get_dateOfPreAuth(self , obj):
        try: 
            dateOfPreAuth = obj.caseNumber.preAuthID.dateOfPreAuth
        except :
            dateOfPreAuth = ''
        return dateOfPreAuth
    
    def get_hospitalCode(self , obj):
        try:
            hospitalCode = obj.caseNumber.preAuthID.hospitalCode
        except : 
            hospitalCode= ''

        return hospitalCode
    
    

class PostPreAuthQueryListSerializer(serializers.ModelSerializer):
    caseNumber = serializers.CharField(max_length=100 , required=True)
    
    class Meta:
        model = PreAuthQuery
        fields = ('caseNumberId' , 'caseNumber', 'query' , 'documents' , )

    def validate(self, data):
        if 'caseNumber' not in data or data['caseNumber'] == "":
            raise serializers.ValidationError('Case Number field can not be empty !!')
        if 'query' not in data or data['query'] == '':
            raise serializers.ValidationError('Query filed can not be empty !!')
        
        return data



class GetClaimQueryListSerializer(serializers.ModelSerializer):
    preAuthId = serializers.SerializerMethodField()
    class Meta:
        model = MPClaimPaidExcel
        fields = ( 'id', 'preAuthId','caseNumber' ,'claimRaisedDate' ,
                     'claimPaidDate' , 'claimPendingRemarks' , 'ClaimQueryStatus' )

    def get_preAuthId(self, obj):
        try:
            preAuthId = obj.caseNumber.preAuthID.preAuthID
        except : 
            preAuthId = ""  
        return preAuthId 


class PostClaimQueryListSerializer(serializers.ModelSerializer):
    caseNumber = serializers.CharField(max_length=100 , required=True)
    
    class Meta:
        model = ClaimQuery
        fields = ('caseNumberId' , 'caseNumber', 'query' , 'documents' , )

    def validate(self, data):
        if 'caseNumber' not in data or data['caseNumber'] == "":
            raise serializers.ValidationError('Case Number field can not be empty !!')
        if 'query' not in data or data['query'] == '':
            raise serializers.ValidationError('Query filed can not be empty !!')
        
        return data
        