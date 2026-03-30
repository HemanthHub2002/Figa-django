from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_order_confirmation_email(order):
    html_content = render_to_string(
        "emails/order_confirmation.html",
        {"order": order}
    )

    email = EmailMultiAlternatives(
        subject="Payment Successful - Order Confirmed",
        body="Your payment was successful.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.user.email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()