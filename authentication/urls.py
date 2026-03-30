from django.urls import path

from .views import UserRegisterView, UserLoginView

#Password Reset 
from .views import send_otp_mail, verify_otp, reset_password

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name ='signup'),
    path('login/', UserLoginView.as_view(), name ='signin'),

    path('send_otp/', send_otp_mail, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('reset_password/', reset_password, name='reset_password'),
]