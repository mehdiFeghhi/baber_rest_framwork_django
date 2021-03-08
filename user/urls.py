from django.urls import path
from user.views import verify_otp,generate_otp
urlpatterns = [
    path('generate_otp/',generate_otp),
    path('verify_otp/',verify_otp)
]
