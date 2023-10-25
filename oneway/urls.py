from django.urls import path
from .views import OTPView, OTPVerificationView

urlpatterns = [
       path('otp/', OTPView.as_view(), name='otp'),
       path('otp-verification/', OTPVerificationView.as_view(), name='otp_verification'),

]