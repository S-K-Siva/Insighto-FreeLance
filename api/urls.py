from django.urls import path,include
from .views import sendOtpToPhoneNumber,verifyOtpOfPhoneNumber,createUser,endpoints

urlpatterns = [
    path('',endpoints,name="endpoints"),
    path('sendOTP/',sendOtpToPhoneNumber,name="sendOtpToMob"),
    path('verifyOTP/',verifyOtpOfPhoneNumber,name="verifyOtpToMob"),
    path('createUser/',createUser,name="createUser"),
]