from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import MPClaimPaidExcel



@receiver(pre_save, sender=MPClaimPaidExcel)
def update_preAuth_query_status(sender, instance, **kwargs):
    
    ''' Update the Query_status field aftrer Inserting the new excel file 
    if chnages in the query for same CaseNumber '''

    if instance.pk: 
        old_instance = MPClaimPaidExcel.objects.get(pk=instance.pk)
        if old_instance.preauthPendingRemarks != instance.preauthPendingRemarks: 
            instance.preAuthQueryStatus = "Pending" 


@receiver(pre_save, sender=MPClaimPaidExcel)
def update_claim_query_status(sender, instance, **kwargs):
    
    ''' Update the Query_status field aftrer Inserting the new excel file 
    if chnages in the query for same CaseNumber '''

    if instance.pk: 
        old_instance = MPClaimPaidExcel.objects.get(pk=instance.pk)
        if old_instance.claimPendingRemarks != instance.claimPendingRemarks: 
            instance.ClaimQueryStatus = "Pending" 