from django.conf import settings
from twilio.rest import Client 
import random
import requests

url = ''
def send_otp_phone(phone):
    client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    #generating OTP
    otp = random.randint(1000,9999)
    data = client.messages.create(
        body="Please verify the Phone Number by this OTP, {}    - Insighto Tech Team".format(otp),
        from_=settings.TWILIO_NUMBER,
        to="+91"+phone
    )
    print("DATA sent is : ",data)
    return otp
