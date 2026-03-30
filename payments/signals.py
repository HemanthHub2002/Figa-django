from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from payments.utils import send_order_confirmation_email

@receiver(post_save, sender=Payment)
def payment_success_email_trigger(sender, instance, **kwargs):
    if instance.status == "COMPLETED":
        send_order_confirmation_email(instance.order)