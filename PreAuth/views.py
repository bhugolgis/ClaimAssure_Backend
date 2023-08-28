from rest_framework import generics
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from io import BytesIO
from reportlab.pdfgen import canvas
from zipfile import ZipFile
from django.http import HttpResponse
from reportlab.lib.utils import ImageReader
from .models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import os
from ClaimAssurance import settings
import datetime
import zipfile
from rest_framework.views import APIView
import io
from rest_framework import status
import shutil
from ClaimManagement.serializers import *
import logging
from rest_framework import filters

# Get an instance of a logger
logger = logging.getLogger("claimAssure")


def PDFGenerator(images, preAuthID, name):
    buffer_list = []
    max_pdf_size = 400000  # 450 KB
    current_pdf_size = 0
    current_pdf_images = 0
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    file_counter = 1

    for image in images:
        img = Image.open(image)
        max_size = (1280, 1280)
        img.thumbnail(max_size, Image.ANTIALIAS)
        img_file = BytesIO()
        if img.format == "JPEG":
            img.save(img_file, 'JPEG' ,optimize= True, quality = 40)
        elif img.format == "PNG":
            img.save(img_file, 'PNG' ,optimize= True, quality = 40)
        elif img.format == "JPG":
            img.save(img_file, 'JPG'  ,optimize= True, quality = 40)
        img_file_size = img_file.tell()

        if current_pdf_size + img_file_size > max_pdf_size:
            pdf.save()
            buffer_list.append(buffer)
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer)
            current_pdf_size = 0
            current_pdf_images = 0

        img_file.seek(0)
        image_reader = ImageReader(img_file)
        pdf.setPageSize((img.width, img.height))
        pdf.drawImage(image_reader, 0, 0)
        pdf.showPage()
        current_pdf_size += img_file_size
        current_pdf_images += 1

    pdf.save()
    buffer_list.append(buffer)
    zip_buffer = BytesIO()
    date = datetime.datetime.today().date()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for buffer in buffer_list:
            buffer.seek(0)
            zip_file.writestr('{}_{}_{}_{}.pdf'.format(preAuthID, date, name,  file_counter), buffer.read())
            file_counter += 1

    zip_buffer.seek(0)
    return zip_buffer.read()

class PreAuthFormView(generics.GenericAPIView):
    serializer_class = CombinedSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = CombinedSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            personal_info_serializer = PersonalInfoSerializer(data={
                'user': request.user.id,
                'nhmpID': validated_data.get('nhmpID'),
                'nameOfPatient': validated_data.get('nameOfPatient'),
                'adharNumber': validated_data.get('adharNumber'),
                'adharPhotograph': validated_data.get('adharPhotograph'),
                'dob': validated_data.get('dob'),
                'gender': validated_data.get('gender'),
                'mobileNumber': validated_data.get('mobileNumber'),
                'alternativeNumber': validated_data.get('alternativeNumber'),
                'addressLine1': validated_data.get('addressLine1'),
                'addressLine2': validated_data.get('addressLine2'),
                'district': validated_data.get('district'),
                'pincode': validated_data.get('pincode'),
                'rationCardNumber': validated_data.get('rationCardNumber'),
                'rationCardPhotograph': validated_data.get('rationCardPhotograph')})

            if personal_info_serializer.is_valid():
                personal_info = personal_info_serializer.save()
            
            else:
                key , value = list(personal_info_serializer.errors.items())[0]
                error_message = key+" ,"+ value[0]
                return Response({'status': 'error', 'message': error_message})

            # Genrating Sequential Preauth ID
            Last_ID = PreAuthDocument.objects.order_by('preAuthID').last()
            if Last_ID:
                preAuthID = 'PRE{:03}'.format(
                    int(Last_ID.preAuthID[3:]) + 1)
            else:
                preAuthID = 'PRE001'

            date = datetime.datetime.today().date()
            files = {}
            for field in ['justification', 'on_BedPhotograph', 'admitCaseSheet', 'labReport']:
                images = request.FILES.getlist(field)

                if images:
                    for image in images:
                        if image.size > 2000 * 1024:
                            return Response({'status': 'error',
                                             'message': 'Each Image size should be less than 1.99 MB - {name}'.format(name=image.name)}, 
                                             status=400)
                        
                    pdf = PDFGenerator(images, preAuthID, field)
                    files[field] = SimpleUploadedFile(
                        f"{preAuthID}_{date}_{field}.zip", pdf, content_type='application/zip'
                    )
            radiology_files = request.FILES.getlist('radiologyReport')

            for i in radiology_files and radiology_files:
                if i.name.endswith('.wrf'):
            # print(radiology_files.filename)
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                            for file in radiology_files:
                                # Save the original file to disk temporarily
                                file_path = os.path.join(
                                    os.path.dirname(file.name), file.name)
                                with open(file_path, 'wb+') as destination:
                                    for chunk in file.chunks():
                                        destination.write(chunk)
                                # Add the file to the ZIP archive
                                zip_file.write(file_path, os.path.basename(file_path))
                                # Remove the temporary file from disk
                                os.remove(file_path)
                        # Create a SimpleUploadedFile object from the ZIP buffer
                        zip_buffer.seek(0)
                        files['radiology'] = SimpleUploadedFile(f"{preAuthID}_{datetime.datetime.today().date()}_radiology.zip",
                                                                zip_buffer.read(),
                                                                content_type='application/zip')
                else:
                    return Response({'status' : 'error' ,
                                    'message' : 'Only .wrf files are allowed to be uploaded in radiology Reports'} , status= 400)

            preauth_document_serializer = PreAuthDocumentSerializer(data={
                'user': request.user.id,
                'preAuthID': preAuthID,
                'personalInfoID': personal_info.nhmpID,
                'dateOfAdmission': validated_data.get('dateOfAdmission'),
                'dateOfPreAuth': validated_data.get('dateOfPreAuth'),
                'hospitalName': validated_data.get('hospitalName'),
                'hospitalCode': validated_data.get('hospitalCode'),
                'justification': files.get('justification', None),
                'on_BedPhotograph': files.get('on_BedPhotograph', None),
                'admitCaseSheet': files.get('admitCaseSheet', None),
                'labReport': files.get('labReport', None),
                'radiologyReport': files.get('radiologyReport', None), })

            if preauth_document_serializer.is_valid():
                preauth_document_serializer.save()
                return Response({'status': 'success', 'message': 'Data Saved Successfully'})
            else:

                key, value =list(preauth_document_serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error', 'message': error_message} , status=400)
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = key+" ,"+value[0]
            return Response({'status': 'error',
                             'message': error_message} , status=400)

class PersonalInfoPostAPI(generics.GenericAPIView):
    serializer_class = PersonalInfoSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data= data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response({'status': 'success' , 'message': 'data saved successfully'} , status=200)
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = key+" ,"+value[0]
            return Response({'status': 'error',
                             'message': error_message} , status=400)

class PersonalInfoUpdateAPI(generics.GenericAPIView):
    serializer_class = PersonalInfoUpdateSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def patch(self , request,id):
        try:
            instance = PersonalInfo.objects.get(nhmpID=id)
        except:
            return Response({'status': 'error', 
                            'message': 'NHMPID not found'} , status=400)
        
        serializer = self.get_serializer(instance , data = request.data , partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response ({'status' : 'success' , 
                            'message' : 'PersnolInfo updated successfully' } , status=200)
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = key+" ,"+value[0]
            return Response({'status': 'error',
                             'message': error_message} , status=400)

class FilterbynhmpID(generics.GenericAPIView):
    serializer_class = PersonalInfoSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, nhmpID):
        PersonalInformation = PersonalInfo.objects.filter(nhmpID=nhmpID).first()
        if not PersonalInformation:
            return Response({'status': 'error',
                             'message': f'{nhmpID} ID is not found'}, status=400)

        PreAuthData = PreAuthDocument.objects.filter(personalInfoID=PersonalInformation.nhmpID)
        PreAuthDataserializer = PreAuthSearcViewhDocumentSerializer(PreAuthData, many=True).data
        serializer = PersonalInfoSerializer(PersonalInformation).data
        return Response({
            'status': 'success',
            'message': 'Data fetched successfully',
            'personalInfo': serializer,
            'PreAuthData': PreAuthDataserializer,
        })

class SearchFilterbypreAuthID(generics.GenericAPIView):
    serializer_class = PreAuthSearchDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, preAuthID):
        PreAuthData = PreAuthDocument.objects.filter(preAuthID=preAuthID)

        print(PreAuthData)

        if not PreAuthData:
            return Response({'status': 'error',
                             'message': f'{preAuthID} ID is not found'}, status=400)

        PersonalInformation = PersonalInfo.objects.filter(
            nhmpID=PreAuthData[0].personalInfoID.nhmpID)
        print(PersonalInformation)
        serializer = PersonalInfoSerializer(PersonalInformation[0]).data
        PreAuthDataserializer = PreAuthDocumentSerializer(
            PreAuthData, many=True).data

        return Response({'status': 'success',
                        'message': 'Data fetched successfully',
                         'personalInfo': serializer,
                         'PreAuthData': PreAuthDataserializer}, status=200)

class SearchFilterbycaseNumber(generics.GenericAPIView):
    serializer_class = PreAuthSearchDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, caseNumber, **kwargs):
        preauth_documents = PreAuthDocument.objects.filter(
            PreAuth_preAuthID__caseNumber=caseNumber)

        if not preauth_documents:
            return Response({'status': 'error',
                             'message': f'{caseNumber} - This Case Number does not exist'},
                            status=400)
        caseNo = PreAuthLinkcaseNumber.objects.get(caseNumber=caseNumber)
        caseNumber_data = PreAuthLinkcaseNumberSerialzier(caseNo).data
        PersonalInfo = preauth_documents[0].personalInfoID
        persnolInfo_data = PersonalInfoSerializer(PersonalInfo).data
        PreAuth_data = PreAuthSearchDocumentSerializer(preauth_documents[0]).data

        models = [
                ('CaseSheet', CaseSheet, CaseSheetSerializer),
                ('LabTest', LabTest, LabTestSerializer),
                ('Reports', Reports, ReportsSerializer),
                ('DischargeSummary', DischargeSummary, DischargeSummarySerialzer),
                ('DeathSummary', DeathSummary, DeathSummarySerialzer),
                ('BloodDocuments', BloodDocuments, BloodDocumentsSerializer),
                ('ClaimManagemntStatus', ClaimManagemntStatus, ClaimManagemntStatusSerialzer)
                ]

        data = {}
        for model_name, model_class, serializer_class in models:
            try:
                model_instance = model_class.objects.get(caseNumber=caseNumber)
                model_data = serializer_class(model_instance).data
                data[model_name] = model_data

            except model_class.DoesNotExist:
                data[model_name] = None

        casesheet_data = data['CaseSheet']
        labtest_data = data['LabTest']
        reports_data = data['Reports']
        DischargeSummary_data = data['DischargeSummary']
        DeathSummary_data = data['DeathSummary']
        BloodDocuments_data = data['BloodDocuments']
        ClaimManagemntStatus_data = data['ClaimManagemntStatus']


        return Response({
            'status': 'success',
            'message': 'data fetched successfully',
            'caseNumber_detail': caseNumber_data,
            'persnolInfo': persnolInfo_data,
            'preAuth': PreAuth_data ,
            'caseSheet_detail': casesheet_data,
            'labTest_detail': labtest_data ,
            'reports_detail' : reports_data ,
            'dischargeSummary_detail' : DischargeSummary_data ,
            'deathSummary_detail' : DeathSummary_data ,
            'bloodDocuments_detail' : BloodDocuments_data ,
            'Claim_Managemnt_Status' : ClaimManagemntStatus_data
            } , status = 200)
    
class ExistingnhmpIDPreAuthFormPost(generics.GenericAPIView):

    serializer_class = ExistingPreAuthDocumentSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExistingPreAuthDocumentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            Last_ID = PreAuthDocument.objects.order_by('preAuthID').last()
            if Last_ID:
                preAuthID = 'PRE{:03}'.format(int(Last_ID.preAuthID[3:]) + 1)
            else:
                preAuthID = 'PRE001'

            # Extract files from request and generate PDFs
            date = datetime.datetime.today().date()
            files = {}
            for field in ['justification', 'on_BedPhotograph', 'admitCaseSheet', 'labReport' , 'radiologyReport' ]:
                images = request.FILES.getlist(field)

                if images:
                    for image in images:
                        if image.size > 2000 * 1024:
                            return Response({'status': 'error',
                                             'message': 'Each Image size should be less than 1.99 MB - {name}'.format(name=image.name)}, 
                                             status=400)
                        
                    pdf = PDFGenerator(images, preAuthID, field)
                    files[field] = SimpleUploadedFile(
                        f"{preAuthID}_{date}_{field}.zip", pdf, content_type='application/zip'
                    )
            # print(files)
            # radiology_files = request.FILES.getlist('radiologyReport')
            # for i in radiology_files and radiology_files:
            #     if i.name.endswith('.wrf'):
            # # print(radiology_files.filename)
            #             zip_buffer = io.BytesIO()
            #             with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            #                 for file in radiology_files:
            #                     # Save the original file to disk temporarily
            #                     file_path = os.path.join(
            #                         os.path.dirname(file.name), file.name)
            #                     with open(file_path, 'wb+') as destination:
            #                         for chunk in file.chunks():
            #                             destination.write(chunk)
            #                     # Add the file to the ZIP archive
            #                     zip_file.write(file_path, os.path.basename(file_path))
            #                     # Remove the temporary file from disk
            #                     os.remove(file_path)
            #             # Create a SimpleUploadedFile object from the ZIP buffer
            #             zip_buffer.seek(0)
            #             files['radiologyReport'] = SimpleUploadedFile(f"{preAuthID}_{datetime.datetime.today().date()}_radiology.zip",
            #                                                     zip_buffer.read(),
            #                                                     content_type='application/zip')
            #     else:
            #         return Response({'status' : 'error' ,
            #                         'message' : 'Only .wrf files are allowed to be uploaded in radiology Reports'} , status= 400)
         
            # Save pre-authorization document
            preauth_document_serializer = ExistingPreAuthserializer(data={
                'preAuthID': preAuthID,
                'personalInfoID': data.get('personalInfoID'),

                'dateOfAdmission': data.get('dateOfAdmission'),
                'dateOfPreAuth': data.get('dateOfPreAuth'),
                'hospitalName': data.get('hospitalName'),
                'hospitalCode': data.get('hospitalCode'),
                'justification': files.get('justification', None),
                'on_BedPhotograph': files.get('on_BedPhotograph', None),
                'admitCaseSheet': files.get('admitCaseSheet', None),
                'labReport': files.get('labReport', None),
                'radiologyReport': files.get('radiologyReport', None),

            })
            if not preauth_document_serializer.is_valid():
                key, value = list(
                    preauth_document_serializer.errors.items())[0]
                error_message = key+" , "+value[0]
                return Response({'status': 'error',
                                 'message': error_message} , status=400)

            preauth_document_serializer.save(user=request.user)
            return Response({'status': 'success',
                            'message': 'Data Saved Successfully'} , status=201)
        else:
            key, value = list(serializer.errors.items())[0]
            error_message = key+" , "+value[0]
            return Response({
                'status': 'error',
                'message': error_message} , status= 400)

class UpdatePreAuthDocumentView(generics.GenericAPIView):
    serializer_class = PreAuthSearchDocumentUpdateSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def put(self, request, preAuthID, **kwargs):
        try:
            instance = PreAuthDocument.objects.get(preAuthID = preAuthID)
        except PreAuthDocument.DoesNotExist:
            return Response({'status': 'error',
                             'message' : 'PreAuth ID is not found'}, status=400)

        serializer = PreAuthSearchDocumentUpdateSerializer(
            instance, data=request.data, partial=True) 
        if serializer.is_valid():
            validated_data = serializer.validated_data

            files = {}
            date = datetime.datetime.today().date()
        
            for key in ['justification', 'on_BedPhotograph', 'admitCaseSheet', 'labReport' , 'radiologyReport']:
                images = request.FILES.getlist(key)
                if images:
                    for image in images:
                        name = image.name
                        if image.size > 2000 * 1024:
                            return Response({'status': 'error',
                                              'message': 'Each Image size should be less than 1.9 MB - {name}'.format(name=name)}, status=400)

                    zip_file = SimpleUploadedFile(f'{preAuthID}_{date}_{key}.zip', PDFGenerator(
                        images, preAuthID, key), content_type='application/zip')
                    files[key] = zip_file
                else:
                    files[key] = None

            # radiology_files = request.FILES.getlist('radiologyReport')
            # if radiology_files:
            #     zip_buffer = io.BytesIO()
            #     with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            #         for file in radiology_files:
            #             # Save the original file to disk temporarily
            #             file_path = os.path.join(
            #                 os.path.dirname(file.name), file.name)
            #             with open(file_path, 'wb+') as destination:
            #                 for chunk in file.chunks():
            #                     destination.write(chunk)
            #             # Add the file to the ZIP archive
            #             zip_file.write(file_path, os.path.basename(file_path))
            #             # Remove the temporary file from disk
            #             os.remove(file_path)
            #     # Create a SimpleUploadedFile object from the ZIP buffer
            #     zip_buffer.seek(0)
            #     files['radiologyReport'] = SimpleUploadedFile(f"{preAuthID}_{date}_radiologyReport.zip",
            #                                                   zip_buffer.read(),
            #                                                   content_type='application/zip')
            # else:
            #     files['radiologyReport'] = None

            preauth_document_serializer = preauth_document_serializer_update_serializer(instance, data={
                'dateOfAdmission': validated_data.get('dateOfAdmission'),
                'dateOfPreAuth': validated_data.get('dateOfPreAuth'),
                'hospitalName': validated_data.get('hospitalName'),
                'hospitalCode': validated_data.get('hospitalCode'),
                  **files})

            if preauth_document_serializer.is_valid():
                preauth_document_serializer.save(user=request.user)
                return Response({'status': 'success', 'message': 'Data Updated Successfully'}, status=201)
            else:
                key, value = list(
                    preauth_document_serializer.errors.items())[0]
                error_message = key + ", " + value[0]
                return Response({'status': 'error', 'message': error_message}, status=400)
        else:
            key, value = list(serializer.errors.items())[0]
            error_message = key + ", " + value[0]
            return Response({'status': 'error', 'message': error_message}, status=400)



    def patch(self, request, preAuthID, **kwargs):
        try:
            instance = PreAuthDocument.objects.get(preAuthID = preAuthID)
        except PreAuthDocument.DoesNotExist:
            return Response({'status': 'error',
                             'message' : 'PreAuth ID is not found'}, status=400)

        serializer = PreAuthSearchDocumentUpdateSerializer(
            instance, data=request.data, partial=True) 
        if serializer.is_valid():
            validated_data = serializer.validated_data
          
            files = {}
            date = datetime.datetime.today().date()
        
            for key in ['justification', 'on_BedPhotograph', 'admitCaseSheet', 'labReport' , 'radiologyReport']:
                images = request.FILES.getlist(key)
                if images:
                    for image in images:
                        name = image.name
                        if image.size > 2000 * 1024:
                            return Response({'status': 'error',
                                              'message': 'Each Image size should be less than 1.9 MB - {name}'.format(name=name)}, status=400)

                    zip_file = SimpleUploadedFile(f'{preAuthID}_{date}_{key}.zip', PDFGenerator(
                        images, preAuthID, key), content_type='application/zip')
                    files[key] = zip_file
                else:
                    pass
           
            # radiology_files = request.FILES.getlist('radiologyReport')
            # if radiology_files:
            #     zip_buffer = io.BytesIO()
            #     with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            #         for file in radiology_files:
            #             # Save the original file to disk temporarily
            #             file_path = os.path.join(
            #                 os.path.dirname(file.name), file.name)
            #             with open(file_path, 'wb+') as destination:
            #                 for chunk in file.chunks():
            #                     destination.write(chunk)
            #             # Add the file to the ZIP archive
            #             zip_file.write(file_path, os.path.basename(file_path))
            #             # Remove the temporary file from disk
            #             os.remove(file_path)
            #     # Create a SimpleUploadedFile object from the ZIP buffer
            #     zip_buffer.seek(0)
            #     files['radiologyReport'] = SimpleUploadedFile(f"{preAuthID}_{date}_radiologyReport.zip",
            #                                                   zip_buffer.read(),
            #                                                   content_type='application/zip')
            # else:
            #     # files['radiologyReport'] = None
            #     pass
            new_data = {**files}

            if 'dateOfAdmission' in validated_data:
                new_data['dateOfAdmission'] = validated_data['dateOfAdmission']
            if 'dateOfPreAuth' in validated_data:
                new_data['dateOfPreAuth'] = validated_data['dateOfPreAuth']
            if 'hospitalName' in validated_data:
                new_data['hospitalName'] = validated_data['hospitalName']
            if 'hospitalCode' in validated_data:
                new_data['hospitalCode'] = validated_data['hospitalCode']

            preauth_document_serializer = preauth_document_serializer_update_serializer(instance, data= new_data , partial = True)
            
            if preauth_document_serializer.is_valid():
            
                preauth_document_serializer.save(user=request.user)
                return Response({'status': 'success', 'message': 'Data Updated Successfully'}, status=201)
            else:
                key, value = list(
                    preauth_document_serializer.errors.items())[0]
                error_message = key + ", " + value[0]
                return Response({'status': 'error', 'message': error_message}, status=400)
        else:
            key, value = list(serializer.errors.items())[0]
            error_message = key + ", " + value[0]
            return Response({'status': 'error', 'message': error_message}, status=400)

class DeletePreAUth(APIView):
	permission_classes=[IsAuthenticated]
        
	def delete(self,request,preAuthID,*args,**kwargs):
            try:
                instance = PreAuthDocument.objects.get(preAuthID=preAuthID)
            except:
                return Response({'status': 'error', 'message': 'PreAuth Id not found'} , status=400)
            serializer = PreAuthDocumnetDeleteSerializer(instance)
            serializer.delete(instance)
            instance.delete()
            return Response( {'status' : 'success'}, status=status.HTTP_204_NO_CONTENT)



		
        
		# return Response({
		# 	"message":"PreAuth data deleted successfully",
		# 	"status":"success"
		# 	},status=status.HTTP_200_OK)

class DownloadPreAuthZipFile(APIView):
    # serializer_class = DownloadPreAuthZipFileSerializer
    parser_classes = [MultiPartParser]
    
    def get(self, request, preAuthID , choice = None):
        try:
            pre_auth_document = PreAuthDocument.objects.filter(
                preAuthID=preAuthID).latest('date_modified')
           
        except PreAuthDocument.DoesNotExist:
            return Response({'status': 'error',
                             'message': 'PreAuth ID not Found'},
                              status=400)
     
        date = datetime.datetime.today().date()
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{name}_{date}_PreAuth_Documents.zip"'.format(name=preAuthID, date=date)
        zip_file = zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED)

        for field_name in ['justification', 'on_BedPhotograph', 'admitCaseSheet', 'labReport', 'radiologyReport']:
            field = getattr(pre_auth_document, field_name)
            try:
                if field and field.file:
                    with zipfile.ZipFile(field.file, 'r') as zip_ref:
                        for zip_info in zip_ref.infolist():
                            zip_info.filename = os.path.basename(zip_info.filename)
                            zip_file.writestr(zip_info, zip_ref.read(zip_info.filename))
            except:
                # logger.error('Unable to read field %s on the server', preAuthID) 
                return Response({'status': 'error',
                                  'message': 'The file you are attempting to download does not exist on server'} , status=400)
          
        zip_file.close()
        if choice == 'SP':
            try:
                share_path = '//192.168.1.7/SharePath/Download'
                filename = response.get('Content-Disposition').split('filename=')[1].replace('"', '')
                zip_file_path = os.path.join(share_path, filename)
            
                with open(zip_file_path, 'wb') as f:
                    f.write(response.content)

                # logger.warning(f'PreAuth Zip File:{zip_file_path} downloaded on Share Path at ' + str(datetime.datetime.now())+' hours!'  )
                # Return a success response
                return Response({'status': 'success',
                                'message': 'File downloaded and saved to share path successfully'} , status=200)
            except:
                return Response({'status': 'error', 'message': 'Share Path could not be found'} , status=404)
        elif choice == 'PC':
            # logger.warning(f'PreAuth Zip File downloaded for ID - {preAuthID} ' +str(datetime.datetime.now()) +' hours!'  )
            return response
        else:
            return Response({'status': 'error', 'message': 'Invalid choice for download'}, status= 400)

class LinkingcaseNumberView(generics.GenericAPIView):
    serializer_class = caseNumberLinkingSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        case_number = request.data['caseNumber']
        try:
            linked_case_number = PreAuthLinkcaseNumber.objects.get(caseNumber = case_number)
            serializer = self.get_serializer(linked_case_number , data=request.data , partial = True )
            if serializer.is_valid():
                serializer.save(user = request.user)
                return Response({'message': 'Data Saved Successfully',
                                'status': 'success'} , status= status.HTTP_200_OK)
            else:
                key, value = list(serializer.errors.items())[0]
                error_message = key+" , "+value[0]
                return Response({'message': error_message,
                                'status': 'error'} , status= status.HTTP_400_BAD_REQUEST)
        except:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user = request.user)
                return Response({'message': 'Data Saved Successfully',
                                'status': 'success'} ,  status= status.HTTP_200_OK)
            else:
                key, value = list(serializer.errors.items())[0]
                error_message = key+" , "+value[0]
                return Response({'message': error_message,
                                'status': 'error'} ,  status= status.HTTP_400_BAD_REQUEST)

class PreAuthEnhancementPostAPI(generics.GenericAPIView):

    serializer_class = PreAuthEnhancementPostSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self , request):
        serializer = self.get_serializer(data = request.data)
        try:
            if serializer.is_valid():
                diffrenece = (datetime.datetime.today().date() - serializer.validated_data['preAuthID'].dateOfPreAuth.date()).days
                # print(int(diffrenece))
                # print(serializer.validated_data['preAuthID'].dateOfPreAuth.date())
                # if diffrenece <= 2:
                serializer.save(user = request.user)
                return Response({'message': 'Data Saved Successfully',
                                'status': 'success'} , status = 200 )
                # else:
                #     return Response({'message': f" Enhancemnet request time is over for preAuthID - {serializer.validated_data['preAuthID']} ",
                #                     'status': 'error'}, status=400)
                
            else:
                key, value = list(serializer.errors.items())[0]

                error_message = key+" , "+value[0]
                return Response({'message': error_message,
                                'status': 'error'} , status = 400)
        except Exception as e :
            logger.error(f"error occured in {request.path}",exc_info=True)
            return Response({'message' : 'Something went wrong'})
        
class PreAuthEnhancementGetAPi(generics.GenericAPIView):
    
    serializer_class = PreAuthEnhancementGetSerializer
    def get(self, request,preAuthID, *args, **kwargs):
        try:
            data = PreAuthEnhancement.objects.filter(preAuthID_id__preAuthID= preAuthID)
        except PreAuthEnhancement.DoesNotExist:
            return Response({'status': 'error',
                             'message': f'No data found for preAuthID - {preAuthID}'}, status=400)
        
        serializer = self.get_serializer( data , many = True).data
        # print(serializer.preAuthID)
        return Response({'status': 'success',
                         'message': 'Data fetch successfully',
                        'data': serializer}, status = 200)
        