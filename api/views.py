from django.shortcuts import render
import json
from rest_framework import serializers
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from users.helpers import send_otp_phone
from users.models import PhoneNumbers, User, Profile
from rest_framework.response import Response
from .serializers import UserModelSerializer, PhoneNumberModelSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,login
from rest_framework.permissions import IsAuthenticated
@api_view(['GET'])
def endpoints(request):
    paths = [
        {"POST:","api/sendOTP"},
        {"POST:","api/verifyOTP"},
        {"POST:","api/createUser"},
        {"POST:","api/userLogin"},
        {"POST:","api/userLogout"},
        {"POST:","api/phoneExist"},
        {"POST:","api/updateProfile"},
    ]
    
    return Response(paths)

# mobile verifcations...
@csrf_exempt
@api_view(['POST'])
def sendOtpToPhoneNumber(request):
    phone = request.data["phone"]
    otp_sent = send_otp_phone(phone)
    obj = None
    try:
        obj = PhoneNumbers.objects.get(phone=phone)
    except:
        obj = None
    if not obj:
        obj = PhoneNumbers.objects.create(phone=phone,otp=otp_sent,is_verified=False)
    serializer = PhoneNumberModelSerializer(obj)
    obj.save()
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def verifyOtpOfPhoneNumber(request):
    try:
        
        user_otp = request.data["otp"]
        phone_number = request.data["phone"]
        obj = PhoneNumbers.objects.get(phone=phone_number)
        
        if str(user_otp).strip() == str(obj.otp).strip():
            # make phoneNumber verified.
            obj.is_verified = True
            serializer = PhoneNumberModelSerializer(data = obj)
            obj.save()
            # return Response(serializer.data)
            return Response("Success")
        else:
            return Response("Failure")
    except Exception as e:
        print(e)
        return Response('Failure')



#user creations.....
@csrf_exempt
@api_view(['POST'])
def createUser(request):
    try:
        phone = request.data["phone"]
        password = request.data["password"]
        username = "Not Updated"
        # phoneObj = PhoneNumbers.objects.get(phone=phone)
        user = User.objects.create(phone=phone,password=password,username=username)
        print("done")
        user.set_password(password)
        print("before serializer")
        serializer = UserModelSerializer(user)
        user.save()
        print("Done...")
        return Response(serializer.data)
        return Response("Success")
    except Exception as e:
        print("E:",e)
        return Response("Failure")


# phone number exist...
@csrf_exempt
@api_view(['POST'])
def phoneExist(request):
    phone = request.data['phone']
    obj = PhoneNumbers.objects.get(phone=phone)
    if obj is None:
        return Response("Failure")
    return Response("Success")

# login
@csrf_exempt
@api_view(['POST'])
def userLogin(request):
    phone = request.data['phone']
    pwd = request.data['pwd']
    user = authenticate(request,phone=phone,password=pwd)
    
    if user.is_authenticated:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        login(request,user)
        return Response({
            "access_token":access_token,
            "refresh_token":str(refresh)
        })
    else:
        return Response("Failure")
# logout 
@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def userLogout(request):
    try:
        refresh_token = request.data['refresh_token']
        print(refresh_token)
        RefreshToken(refresh_token).blacklist()
        return Response("Success")
    except:
        return Response("Failure")


#update profile

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def updateProfile(request):
    try:
        
        username = request.data['username']
        email = request.data['email']
        dob = request.data['dob']
        # highest_education_qualification = request.data['dob']
        city = request.data['city']
        state = request.data['state']
        country = request.data['country']
        linked_in = request.data['linked_in']
        aadhar_number = request.data['aadhar_number']
        profile_photo = request.data['profile_photo']
        
        data = {
            "username":username,
            "email":email,
            "dob":dob,
            "city":city,
            "state":state,
            "country":country,
            "linked_in":linked_in,
            "aadhar_number":aadhar_number,
            "profile_photo":profile_photo
        }
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile,data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"User Profile updated"})
        else:
            return Response(serializer.errors,status=400)
    except:
        return Response("Failure")
# company creation
# def createCompany(request):
#     name = request.data['name']
#     address = request.data['address']
#     industry = request.data['industry']
#     company_logo_url = request.data['']
# role creation
# skill creation