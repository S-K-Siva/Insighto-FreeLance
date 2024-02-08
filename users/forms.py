from django.forms import ModelForm
from .models import User


class UserModelForm(ModelForm):
    model = User
    fields = ['phone','otp','password']
