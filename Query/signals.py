
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import PreAuthQuery, ClaimQuery
from ClaimManagement.models import MPClaimPaidExcel


# Updating the Query status in MPClaimPaidExcel after attending the query
@receiver(pre_save, sender=PreAuthQuery)
def PreAuth_query_status(sender, instance, **kwargs):
    last_field_change = MPClaimPaidExcel.objects.filter(
        preauthPendingRemarks=instance.query, caseNumber=instance.caseNumberId.caseNumber).exists()
    if last_field_change:
        # print(instance.caseNumberId.query_status)
        instance.caseNumberId.preAuthQueryStatus = 'Attended'
        instance.caseNumberId.save()


@receiver(pre_save, sender=ClaimQuery)
def Claim_query_status(sender, instance, **kwargs):
    last_field_change = MPClaimPaidExcel.objects.filter(
        claimPendingRemarks=instance.query, caseNumber=instance.caseNumberId.caseNumber).exists()
    if last_field_change:
        # print(instance.caseNumberId.query_status)
        instance.caseNumberId.ClaimQueryStatus = 'Attended'
        instance.caseNumberId.save()
