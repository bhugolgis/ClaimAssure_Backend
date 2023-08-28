from rest_framework import generics
from PreAuth.models import PreAuthDocument
import datetime
from rest_framework.response import Response
from .serializers import *
from ClaimManagement.models import MPClaimPaidExcel
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.db.models import Q


class DashboardAPI(generics.GenericAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = DashboardAPISerailizer
    queryset = MPClaimPaidExcel.objects.all()
    def get(self , request ):
        try:
            choice = request.data["Choice"]

            if choice == "Today":
                print("TOday")
                count_of_preAuth = PreAuthDocument.objects.filter(date_modified__date = datetime.date.today() ).count()
                count_of_PreAuth_Query = self.get_queryset().exclude(preauthPendingRemarks__exact = '').filter(date_modified__date = datetime.date.today() ).count()
                attended_PreAuth_query = self.get_queryset().filter(preAuthQueryStatus = "Attended").filter(date_modified__date = datetime.date.today() ).count()
                count_of_Claim_Query = self.get_queryset().exclude(claimPendingRemarks__exact = '').filter(date_modified__date = datetime.date.today() ).count()
                attended_Claim_query = self.get_queryset().filter(ClaimQueryStatus = "Attended").filter(date_modified__date = datetime.date.today() ).count()
                penidng_Claim_query = self.get_queryset().filter(ClaimQueryStatus = "Pending").exclude(claimPendingRemarks__exact = '').filter(date_modified__date = datetime.date.today() ).count()
                Pending_PreAuth_query = self.get_queryset().filter(preAuthQueryStatus = "Pending").exclude(preauthPendingRemarks__exact = '').filter(date_modified__date = datetime.date.today() ).count() 
                
                return Response({"count_of_preAuth" : count_of_preAuth , 
                                "total_Query_count" : count_of_PreAuth_Query + count_of_Claim_Query , 
                                "count_of_PreAuth_Query" : count_of_PreAuth_Query,
                                "attended_PreAuth_query" : attended_PreAuth_query,
                                "Pending_PreAuth_query" : Pending_PreAuth_query , 
                                "count_of_Claim_Query" : count_of_Claim_Query,
                                "attended_Claim_query" : attended_Claim_query ,
                                "penidng_Claim_query" : penidng_Claim_query
                                })

            elif choice == "Last 7 Days":
                start_date = datetime.date.today() 
                end_date = start_date - datetime.timedelta(days=7)
                count_of_preAuth = PreAuthDocument.objects.filter(date_modified__date__range = (end_date , start_date)).count()
                count_of_PreAuth_Query = self.get_queryset().exclude(preauthPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count()
                attended_PreAuth_query = self.get_queryset().filter(preAuthQueryStatus = "Attended").filter(date_modified__date__range = (end_date , start_date)).count()
                count_of_Claim_Query = self.get_queryset().exclude(claimPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count()
                attended_Claim_query = self.get_queryset().filter(ClaimQueryStatus = "Attended").filter(date_modified__date__range = (end_date , start_date)).count()
                penidng_Claim_query = self.get_queryset().filter(ClaimQueryStatus = "Pending").exclude(claimPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count()
                Pending_PreAuth_query = self.get_queryset().filter(preAuthQueryStatus = "Pending").exclude(preauthPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count() 
                
                return Response({"count_of_preAuth" : count_of_preAuth , 
                                "total_Query_count" : count_of_PreAuth_Query + count_of_Claim_Query , 
                                "count_of_PreAuth_Query" : count_of_PreAuth_Query,
                                "attended_PreAuth_query" : attended_PreAuth_query,
                                "Pending_PreAuth_query" : Pending_PreAuth_query , 
                                "count_of_Claim_Query" : count_of_Claim_Query,
                                "attended_Claim_query" : attended_Claim_query ,
                                "penidng_Claim_query" : penidng_Claim_query
                                })
            
            elif choice ==  "Last 30 Days" :
                start_date = datetime.date.today() 
                end_date = start_date - datetime.timedelta(days=30)
                count_of_preAuth = PreAuthDocument.objects.filter(date_modified__date__range = (end_date , start_date)).count()
                count_of_PreAuth_Query = self.get_queryset().exclude(preauthPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count()
                attended_PreAuth_query = self.get_queryset().filter(preAuthQueryStatus = "Attended").filter(date_modified__date__range = (end_date , start_date)).count()
                count_of_Claim_Query = self.get_queryset().exclude(claimPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count()
                attended_Claim_query = self.get_queryset().filter(ClaimQueryStatus = "Attended").filter(date_modified__date__range = (end_date , start_date)).count()
                penidng_Claim_query = self.get_queryset().filter(ClaimQueryStatus = "Pending").exclude(claimPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count()
                Pending_PreAuth_query = self.get_queryset().filter(preAuthQueryStatus = "Pending").exclude(preauthPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count() 
                
                return Response({"count_of_preAuth" : count_of_preAuth , 
                                "total_Query_count" : count_of_PreAuth_Query + count_of_Claim_Query , 
                                "count_of_PreAuth_Query" : count_of_PreAuth_Query,
                                "attended_PreAuth_query" : attended_PreAuth_query,
                                "Pending_PreAuth_query" : Pending_PreAuth_query , 

                                "count_of_Claim_Query" : count_of_Claim_Query,
                                "attended_Claim_query" : attended_Claim_query ,
                                "penidng_Claim_query" : penidng_Claim_query
                                }) 
            elif choice ==  "Last 3 Months" :
                start_date = datetime.date.today() 
                end_date = start_date - datetime.timedelta(days= 90)
                count_of_preAuth = PreAuthDocument.objects.filter(date_modified__date__range = (end_date , start_date)).count()
                count_of_PreAuth_Query = self.get_queryset().exclude(preauthPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count()
                attended_PreAuth_query = self.get_queryset().filter(preAuthQueryStatus = "Attended").filter(date_modified__date__range = (end_date , start_date)).count()
                count_of_Claim_Query = self.get_queryset().exclude(claimPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count()
                attended_Claim_query = self.get_queryset().filter(ClaimQueryStatus = "Attended").filter(date_modified__date__range = (end_date , start_date)).count()
                penidng_Claim_query = self.get_queryset().filter(ClaimQueryStatus = "Pending").exclude(claimPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count()
                Pending_PreAuth_query = self.get_queryset().filter(preAuthQueryStatus = "Pending").exclude(preauthPendingRemarks__exact = '').filter(date_modified__date__range = (end_date , start_date)).count() 
                
                return Response({"count_of_preAuth" : count_of_preAuth , 
                                "total_Query_count" : count_of_PreAuth_Query + count_of_Claim_Query , 
                                "count_of_PreAuth_Query" : count_of_PreAuth_Query,
                                "attended_PreAuth_query" : attended_PreAuth_query,
                                "Pending_PreAuth_query" : Pending_PreAuth_query , 

                                "count_of_Claim_Query" : count_of_Claim_Query,
                                "attended_Claim_query" : attended_Claim_query ,
                                "penidng_Claim_query" : penidng_Claim_query
                                })
        
        except:
            count_of_preAuth = PreAuthDocument.objects.all().count()
            count_of_PreAuth_Query = self.get_queryset().exclude(preauthPendingRemarks__exact = '').count()
            attended_PreAuth_query = self.get_queryset().filter(preAuthQueryStatus = "Attended").count()
            count_of_Claim_Query = self.get_queryset().exclude(claimPendingRemarks__exact = '').count()
            attended_Claim_query = self.get_queryset().filter(ClaimQueryStatus = "Attended").count()
            penidng_Claim_query = self.get_queryset().filter(ClaimQueryStatus = "Pending").exclude(claimPendingRemarks__exact = '').count()
            Pending_PreAuth_query = self.get_queryset().filter(preAuthQueryStatus = "Pending").exclude(preauthPendingRemarks__exact = '').count() 
            
            return Response({"count_of_preAuth" : count_of_preAuth , 
                             "total_Query_count" : count_of_PreAuth_Query + count_of_Claim_Query , 
                            "count_of_PreAuth_Query" : count_of_PreAuth_Query,
                            "attended_PreAuth_query" : attended_PreAuth_query,
                            "Pending_PreAuth_query" : Pending_PreAuth_query , 
                             "count_of_Claim_Query" : count_of_Claim_Query,
                             "attended_Claim_query" : attended_Claim_query ,
                             "penidng_Claim_query" : penidng_Claim_query
                             })