from rest_framework.serializers import ModelSerializer
from users.models import User,PhoneNumbers,Jobs,Profile,Experience,Skills,Applications
from company.models import Company,Role,Skill
# User
class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class PhoneNumberModelSerializer(ModelSerializer):
    class Meta:
        model = PhoneNumbers 
        fields = "__all__"

class JobsSerializer(ModelSerializer):
    class Meta:
        model = Jobs
        fields = "__all__"

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class SkillsSerializer(ModelSerializer):
    class Meta:
        model = Skills 
        fields = "__all__"
    
class ApplicationsSerializer(ModelSerializer):
    class Meta:
        model = Applications
        fields = "__all__"

    
# company
class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
    
class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill 
        fields = "__all__"

