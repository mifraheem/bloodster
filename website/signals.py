# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BloodRequest
from bloodster.email_functions import send_request_email


@receiver(post_save, sender=BloodRequest)
def notify_status_change(sender, instance, **kwargs):
    if instance.status in ['in_progress', 'fulfilled', 'cancelled']:
        recipient_email = instance.recipient.email
        donor_email = instance.fulfilled_by.email if instance.fulfilled_by else None
        if recipient_email and donor_email:
            request_details = {
                'blood_group': instance.requested_blood_group,
                'urgency': instance.urgency,
                'location': instance.location,
                'additional_info': instance.additional_info
            }
            send_request_email(recipient_email, donor_email,
                               instance.status, request_details)
