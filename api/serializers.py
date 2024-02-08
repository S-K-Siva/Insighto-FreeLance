from rest_framework.serializers import ModelSerializer
from users.models import User,PhoneNumbers

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PhoneNumberModelSerializer(ModelSerializer):
    class Meta:
        model = PhoneNumbers 
        fields = "__all__"




    

