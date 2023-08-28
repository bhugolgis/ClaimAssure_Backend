from rest_framework import generics
from rest_framework.views import APIView
from .serializers import *
from ClaimManagement.models import *
from rest_framework.response import Response 
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
import datetime
from PreAuth.views import PDFGenerator
from django.core.files.uploadedfile import SimpleUploadedFile
import zipfile
from django.http import HttpResponse
import os
from rest_framework import filters
from rest_framework import status
from .utils import util
from ClaimManagement.paginations import LimitsetPagination
class SearchFieldsForPreAuthQueryList(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if 'caseNumber__caseNumber' in request.GET or 'caseNumber__preAuthID__preAuthID' in request.GET:
            return ['caseNumber__caseNumber', 'caseNumber__preAuthID__preAuthID']
        return super().get_search_fields(view, request)
    
class GetPreAuthQueryList(generics.ListAPIView):
    serializer_class = GetPreAuthQueryListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFieldsForPreAuthQueryList]
    pagination_class = LimitsetPagination
    search_fields = ['caseNumber__caseNumber' , 'caseNumber__preAuthID__preAuthID' ]

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
    
    def get_queryset(self): 
        # return MPClaimPaidExcel.objects.all().exclude(preauthPendingRemarks__exact = '' ).exclude(preAuthQueryStatus ='Attended')
        return MPClaimPaidExcel.objects.all().exclude(preauthPendingRemarks__exact = '')
    
    def get(self, request):
        serializers = self.get_serializer(self.filter_queryset(self.get_queryset()) , many = True).data
        if serializers:
            return Response({"status" : "success" ,
                            "message" : "Data retrieved successfully",
                            'data': serializers} , status = 200)
        else:
            return Response({"status" : "error",
                            "message" : "No Data found"} , status = 200)
        
class PostPreAuthQuery(generics.GenericAPIView):
    serializer_class = PostPreAuthQueryListSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request ):
       
        caseNumber = request.data['caseNumber'].replace('/', '')
        date = datetime.datetime.today().date()
        files = {}
        for field in ['documents']:

            images = request.FILES.getlist(field)
            if images:
                for image in images:
                    if image.size > 2000 * 1024:
                        return Response({'status': 'error', 'message': 'Each Image size should be less than 1.99 MB'}, status=status.HTTP_400_BAD_REQUESTs)
                pdf = PDFGenerator(images, caseNumber, field)
                files[field] = SimpleUploadedFile(f"{caseNumber}_{date}_{field}.zip", pdf, content_type='application/zip')

        serializer = self.get_serializer(data ={
            'caseNumberId' : request.data['caseNumberId'] ,
            'caseNumber': request.data['caseNumber'],
            'query' : request.data['query'] , 
            **files})
        
        if serializer.is_valid():
            caseNumber = serializer.validated_data.pop('caseNumber')
            check_status = MPClaimPaidExcel.objects.filter(id=request.data['caseNumberId'] , 
                                                           preauthPendingRemarks = request.data['query'] , preAuthQueryStatus = 'Attended').exists()
            if check_status:
                return Response({'message' : 'Query Already attended', 'status' : 'error'}, status=400)
            
            serializer.save(user = request.user)
            return Response({"status": "success" ,
                            "message": "Data saved successfully",
                            } , status = 200)
        else:
            return Response({"status": "error",
                            "message": "No Data found"} , status= status.HTTP_400_BAD_REQUEST)

class DownloadPreAuthQueryDocument(APIView):

    parser_classes = [MultiPartParser]
    
    def get (self, request , id , choice  ):
        try:
            PreAuthQueryDocument = PreAuthQuery.objects.filter(
                caseNumberId_id= id).latest('date_modified')
           
        except PreAuthQuery.DoesNotExist:
            return Response({'status': 'error',
                             'message': 'CaseNumber not Found'},
                              status=400)
        caseNumber = PreAuthQueryDocument.caseNumberId.caseNumber.caseNumber.replace('/', '')
        date = datetime.datetime.today().date()
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{name}_{date}_Query_Documents.zip"'.format(
            name=caseNumber, date=date)
        zip_file = zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED)


        for field_name in [ 'documents']:
            field = getattr(PreAuthQueryDocument, field_name)
            try:
                if field and field.file:
                    with zipfile.ZipFile(field.file, 'r') as zip_ref:
                        for zip_info in zip_ref.infolist():
                            zip_info.filename = os.path.basename(zip_info.filename)
                            zip_file.writestr(zip_info, zip_ref.read(zip_info.filename))
            except:
                # logger.warning('Unable to read field %s on the server', caseNumber) 
                return Response({'status': 'error',
                                  'message': 'The file you are attempting to download does not exist on server'} , status=status.HTTP_400_BAD_REQUEST)

        zip_file.close()
        if choice == 'SP':
            share_path = '//192.168.1.7/SharePath/Download'
            filename = response.get('Content-Disposition').split('filename=')[1].replace('"', '')
            zip_file_path = os.path.join(share_path, filename)

            with open(zip_file_path, 'wb') as f:
                f.write(response.content)

            # logger.warning(f'PreAuth Zip File:{zip_file_path} downloaded on Share Path at ' +str(datetime.datetime.now())+' hours!'  )
            # Return a success response
            return Response({'status': 'success',
                            'message': 'File downloaded and saved to share path successfully'} , status=200)
        elif choice == 'PC':
            # logger.warning(f'PreAuth Zip File downloaded for ID - {preAuthID} ' +str(datetime.datetime.now()) +' hours!'  )
            return response
        else:
            return Response({'status': 'error', 'message': 'Invalid choice for download'}, status= status.HTTP_400_BAD_REQUEST)

class SearchFieldsForClaimQueryList(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if 'caseNumber__caseNumber' in request.GET or 'caseNumber__preAuthID__preAuthID' in request.GET:
            return ['caseNumber__caseNumber', 'caseNumber__preAuthID__preAuthID']
        return super().get_search_fields(view, request)
    
class GetClaimQueryList(generics.GenericAPIView):
 
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFieldsForClaimQueryList]
    search_fields = ['caseNumber__caseNumber' , 'caseNumber__preAuthID__preAuthID' ]
    serializer_class = GetClaimQueryListSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
    
    def get_queryset(self): 
        return MPClaimPaidExcel.objects.all().exclude(claimPendingRemarks__exact = '')
        # return MPClaimPaidExcel.objects.all().exclude(claimPendingRemarks__exact = '').exclude(ClaimQueryStatus = 'Attended')
    
    def get(self, request, *args, **kwargs):
        serializers =  self.get_serializer(self.filter_queryset(self.get_queryset()) , many = True).data

        if serializers:
            return Response({"status": "success" ,
                            "message": "Data retrieved successfully",
                            'data': serializers} , status = 200)
        else:
            return Response({"status": "error",
                            "message": "No Data found"})
        
class PostClaimQuery(generics.GenericAPIView):
    serializer_class = PostClaimQueryListSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request ):
        try:
            caseNumber = request.data['caseNumber'].replace('/', '')
        except:
            return Response({'status': 'error', 'message': 'caseNumber is not provided'}, status=400)

        date = datetime.datetime.today().date()
        files = {}
        for field in ['documents']:

            images = request.FILES.getlist(field)
            if images:
                for image in images:
                    if image.size > 2000 * 1024:
                        return Response({'status': 'error', 'message': 'Each Image size should be less than 1.99 MB'}, status=status.HTTP_400_BAD_REQUEST)
                pdf = PDFGenerator(images, caseNumber, field)
                files[field] = SimpleUploadedFile(
                    f"{caseNumber}_{date}_{field}.zip", pdf, content_type='application/zip')

        serializer = self.get_serializer(data ={
            'caseNumberId' : request.data['caseNumberId'] , 
            'caseNumber': request.data['caseNumber'] ,
            'query' : request.data['query'] , 
            **files})
        
        if serializer.is_valid():
            caseNumber = serializer.validated_data.pop('caseNumber')
            check_status = MPClaimPaidExcel.objects.filter(id=request.data['caseNumberId'] , 
                                                           claimPendingRemarks = request.data['query'] , ClaimQueryStatus = 'Attended').exists()
            if check_status:
                return Response({'message' : 'Query Already attended', 'status' : 'error'}, status=400)
            
            serializer.save(user = request.user)
            return Response({"status": "success" ,
                            "message": "Data saved successfully",
                            } , status = 200)
        else:
            return Response({"status": "error",
                            "message": "No Data found"} , status= status.HTTP_400_BAD_REQUEST)

class DownloadClaimQueryDocument(APIView):
    
    parser_classes = [MultiPartParser]

    def get (self, request , id , choice  ):
        try:
            ClaimQueryDocument = ClaimQuery.objects.filter(
                caseNumberId_id= id).latest('date_modified')
            
        except ClaimQuery.DoesNotExist:
            return Response({'status': 'error',
                             'message': 'CaseNumber not Found'},
                              status=status.HTTP_400_BAD_REQUEST)
        caseNumber = ClaimQueryDocument.caseNumberId.caseNumber.caseNumber.replace('/', '')
    
        date = datetime.datetime.today().date()
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{name}_{date}_Query_Documents.zip"'.format(
            name=caseNumber, date=date)
        zip_file = zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED)


        for field_name in [ 'documents']:
            field = getattr(ClaimQueryDocument, field_name)
            try:
                if field and field.file:
                    with zipfile.ZipFile(field.file, 'r') as zip_ref:
                        for zip_info in zip_ref.infolist():
                            zip_info.filename = os.path.basename(zip_info.filename)
                            zip_file.writestr(zip_info, zip_ref.read(zip_info.filename))
            except:
                # logger.warning('Unable to read field %s on the server', caseNumber) 
                return Response({'status': 'error',
                                  'message': 'The file you are attempting to download does not exist on server'} , status= status.HTTP_400_BAD_REQUEST)

        zip_file.close()
        if choice == 'SP':
            share_path = '//192.168.1.7/SharePath/Download'
            filename = response.get('Content-Disposition').split('filename=')[1].replace('"', '')
            
            zip_file_path = os.path.join(share_path, filename)
            with open(zip_file_path, 'wb') as f:
                f.write(response.content)

            # logger.warning(f'PreAuth Zip File:{zip_file_path} downloaded on Share Path at ' +str(datetime.datetime.now())+' hours!' )
            # Return a success response
            return Response({'status': 'success',
                            'message': 'File downloaded and saved to share path successfully'} , status= 200)
        elif choice == 'PC':
            # logger.warning(f'PreAuth Zip File downloaded for ID - {preAuthID} ' +str(datetime.datetime.now()) +' hours!' )
            return response
        else:
            return Response({'status': 'error', 'message': 'Invalid choice for download'}, status= status.HTTP_400_BAD_REQUEST)

class DeletePreAuthQuery(generics.GenericAPIView):
    def delete(self, request , id ):
        try:
            instance = PreAuthQuery.objects.get(caseNumberId_id = id)
        except:
            return Response({   'status': 'error',
                                'message': 'Invalid choice for deletion'} , status= status.HTTP_400_BAD_REQUEST)
        if instance.documents:
            instance.documents.delete()
        instance.delete()
        return Response({'status': 'success',
                          'message': 'Deleted PreAuth query documnts'})

import json
import glob
import os


def send_email():
    emails = ['jafar.khan@bhugolgis.com' , 'jafarkhan9892@gmail.com']
    for email in emails:
        data = {
            'subject':'File is not Updated' , 
            'body' : f'last file was recived at  please check for Updates' , 
            'to_email': email
            }
        # util.send_email(data)
   
        return util.send_email(data)


class JSONFileView(generics.GenericAPIView):

    
    def get(self , request):
        list_of_files =glob.iglob('//192.168.1.7/SharePath/Download/*.json')
        latest_file = max(list_of_files, key=os.path.getmtime)
        today_hour = datetime.datetime.today().hour
        last_file_time =  datetime.datetime.fromtimestamp(os.path.getctime(latest_file)).hour
        hour_diffrence = today_hour - last_file_time 
       
        if hour_diffrence >= 2:
            send_email()
            return Response( {'message': 'Email sent successfully'})
        else:
            with open(latest_file, 'r') as jsonfile:
                json_data = json.load(jsonfile)
            return Response(json_data)
        