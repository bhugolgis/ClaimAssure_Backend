from rest_framework import serializers
from .models import *


class ExcelFileSerializer(serializers.Serializer):
    file = serializers.FileField()

class CaseSheetSerializer(serializers.ModelSerializer):
    # caseNumber = serializers.CharField(max_length=100 , required=True)
    class Meta:
        model =  CaseSheet
        fields = ( 'caseNumber' , 'admitCaseClinicalSheet' , 'icp' , 'medicationChart' ,'initialSheet' ,
                     'tprChart' , 'vitalChart' , 'losStayChart' , 'caseSheetOtherDocuments')
        
        def validate(self , data):
            if 'caseNumber' not in data or data['caseNumber'] == "":
                raise serializers.ValidationError('Case number field can not be empty')
            
            return data
    
class CaseSheetUpdateSerializer(serializers.ModelSerializer):  
    class Meta:
        model = CaseSheet
        fields = ( 'admitCaseClinicalSheet' , 'icp' , 'medicationChart' ,'initialSheet' ,
                     'tprChart' , 'vitalChart' , 'losStayChart' , 'caseSheetOtherDocuments')   

class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ( 'caseNumber', 'microbiology' ,'biochemistry' , 'pathology' ,'serologyInvestigation' , 'labTestOtherDocuments')

    def validate(self , data):
        if 'caseNumber' not in data or data['caseNumber'] == "":
            raise serializers.ValidationError('Case number field can not be empty')
        
        return data
class LabTestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ('microbiology' ,'biochemistry' , 'pathology' ,'serologyInvestigation' , 'labTestOtherDocuments')

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = (  'caseNumber' , 'radiology' , 'otprocedureSheets' , 'anaesthesiaNotes' , 'anaesthesiaNotes' , 'reportsOtherDocuments')

    def validate(self , data):
        if 'caseNumber' not in data or data['caseNumber'] == "":
            raise serializers.ValidationError('Case number field can not be empty')
        
        return data
class ReportsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ('radiology' , 'otprocedureSheets' , 'anaesthesiaNotes' , 'anaesthesiaNotes' , 'reportsOtherDocuments')
    
    
class DischargeSummarySerialzer(serializers.ModelSerializer):
    class Meta:
        model = DischargeSummary
        fields = ( 'caseNumber' , 'dischargeDate' , 'dischargeType' , 'dischargeSummaryDocument' , 'dischargeSummaryOtherDocuments')

    def validate(self , data):
        if 'caseNumber' not in data or data['caseNumber'] == "":
            raise serializers.ValidationError('Case number field can not be empty')
        
        return data
class DischargeSummaryUpdateSerialzer(serializers.ModelSerializer):
    class Meta:
        model = DischargeSummary
        fields = ('dischargeDate' , 'dischargeType' , 'dischargeSummaryDocument' , 'dischargeSummaryOtherDocuments')

class GetLinkedCaseNumberListserialzier(serializers.ModelSerializer):
    class Meta:
        model = PreAuthLinkcaseNumber
        fields = ('caseNumber' , 'date_modified')
class DeathSummarySerialzer(serializers.ModelSerializer):
    class Meta:
        model = DeathSummary
        fields = ( 'caseNumber' , 'mortalityAudit' ,'deathCertificate',
                  'deathSummaryOtherDocuments')
    
    def validate(self , data):
        if 'caseNumber' not in data or data['caseNumber'] == "":
            raise serializers.ValidationError('Case number field can not be empty')
        
        return data
class DeathSummaryUpdateSerialzer(serializers.ModelSerializer):
    class Meta:
        model = DeathSummary
        fields = ('mortalityAudit' ,'deathCertificate',
                  'deathSummaryOtherDocuments')
class BloodDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloodDocuments
        fields = ( 'caseNumber' , 'bloodTransfusion' , 'btSticker' , 'crossMatchReport' , 'bloodOtherDocuments')

    def validate(self , data):
        if 'caseNumber' not in data or data['caseNumber'] == "":
            raise serializers.ValidationError('Case number field can not be empty')
        
        return data

class BloodDocumentsUpdateSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = BloodDocuments
        fields = ('bloodTransfusion' , 'btSticker' , 'crossMatchReport' , 'bloodOtherDocuments')


class ClaimManagemntStatusSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ClaimManagemntStatus
        fields = ('caseNumber','status',)
    
    def validate(self , data):
        if 'caseNumber' not in data or data['caseNumber'] == "":
            raise serializers.ValidationError('Case number field can not be empty')
        
        return data

class DumpExcelSerializer(serializers.Serializer):
    
    excel_file = serializers.FileField(required=True)

class DumpCSVSerializer(serializers.Serializer):
    csv_file = serializers.FileField(required=True)

class DumpExcelViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DumpExcel
        fields = '__all__'