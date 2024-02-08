from django.shortcuts import render
import json
from rest_framework import serializers
from django.http import JsonResponse
from rest_framework.decorators import api_view
from users.helpers import send_otp_phone
from users.models import PhoneNumbers, User
from rest_framework.response import Response
from .serializers import UserModelSerializer, PhoneNumberModelSerializer
from django.views.decorators.csrf import csrf_exempt
@api_view(['GET'])
def endpoints(request):
    paths = [
        {"POST:","api/sendOTP"},
        {"POST:","api/verifyOTP"},
        {"POST:","api/createUser"}
    ]
    
    return Response(paths)
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





