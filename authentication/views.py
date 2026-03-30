from django.shortcuts import render,  redirect
from django.urls import reverse_lazy

# Using the built-in auth app User model
from django.contrib.auth.models import User 

# extending the auth views
from django.contrib.auth.views import (
    LoginView
)
# CreateView CBV
from django.views.generic import CreateView

from .forms import UserRegisterForm, UserLoginForm

from django.contrib.auth import login

# Create your views here.

class UserRegisterView(CreateView):
    model = User 
    form_class = UserRegisterForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('signin')


class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    authentication_form = UserLoginForm

# Password reset flow

import random
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP


def generate_otp():
    return str(random.randint(100000,999999))

def send_otp_mail(request):
    context = None
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            otp = generate_otp()
            EmailOTP.objects.create(email = email, otp = otp)

            # Prepare th email
            subject = "Your OTP code"
            message = f"Your OTP  is {otp}. It will expire in 10 minuts"
            send_mail(
                subject = subject,
                message = message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [email],
                fail_silently = False
            )

            request.session['email_for_reset'] = email
            return redirect('verify_otp')
        context = {
            'error' : "Email missing"
        }

    if not context:
        context = {}

    return render(request,
                  template_name='authentication/pwd_reset/send_otp_email.html',
                  context = context )


def verify_otp(request):
    email = request.session.get('email_for_reset')
    if not email:
        return redirect('send_otp')

    context = {}

    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '')

        try:
            otp_record = EmailOTP.objects.filter(
                email=email, otp=otp_entered
            ).latest('created_at')
        except EmailOTP.DoesNotExist:
            otp_record = None

        if otp_record and not otp_record.is_expired():
            request.session['otp_verified'] = True
            return redirect('reset_password')
        else:
            context['error'] = 'Invalid or expired OTP. Please try again.'

    return render(request,
                  template_name='authentication/pwd_reset/verify_otp.html',
                  context=context)


def reset_password(request):
    email = request.session.get('email_for_reset')
    verified = request.session.get('otp_verified')

    if not email or not verified:
        return redirect('send_otp')

    context = {}

    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if password1 != password2:
            context['error'] = 'Passwords do not match.'
        elif len(password1) < 8:
            context['error'] = 'Password must be at least 8 characters.'
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()

                # Clean up session
                del request.session['email_for_reset']
                del request.session['otp_verified']

                return redirect('signin')
            except User.DoesNotExist:
                context['error'] = 'No account found with this email.'

    return render(request,
                  template_name='authentication/pwd_reset/reset_password.html',
                  context=context)
