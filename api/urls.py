from django.urls import path,include
from .views import sendOtpToPhoneNumber,verifyOtpOfPhoneNumber,createUser,endpoints
from . import views
urlpatterns = [
    path('',endpoints,name="endpoints"),
    path('sendOTP/',sendOtpToPhoneNumber,name="sendOtpToMob"),
    path('verifyOTP/',verifyOtpOfPhoneNumber,name="verifyOtpToMob"),
    path('createUser/',createUser,name="createUser"),
    path('phoneExist/',views.phoneExist,name="phoneExist"),
    path('userLogin/',views.userLogin,name="userLogin"),
    path('userLogout/',views.userLogout,name="userLogout"),
    path('updateProfile/',views.updateProfile,name="updateProfile"),
    path('currentUserJWT/',views.currentUserJWT,name="currentUserJWT"),
]