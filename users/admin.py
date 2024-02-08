from django.contrib import admin
from .models import User, PhoneNumbers, Profile, Applications,Skills,Jobs,Experience
# Register your models here.
admin.site.register(User)
admin.site.register(PhoneNumbers)
admin.site.register(Profile)
admin.site.register(Applications)
admin.site.register(Skills)
admin.site.register(Jobs)
admin.site.register(Experience)