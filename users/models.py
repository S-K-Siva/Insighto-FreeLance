from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MinValueValidator
from .manager import UserManager
from company.models import Company, Skill, Role
import uuid
class PhoneNumbers(models.Model):
    phone = models.CharField(max_length=10,null=False,blank=False,unique=True,validators=[MinLengthValidator(10)]) #91-000-000-0000
    otp = models.CharField(max_length=4,null=False,blank=False,validators=[MinLengthValidator(4)])
    is_verified = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone)


class User(AbstractUser):
    # phone = models.OneToOneField(PhoneNumbers,on_delete=models.CASCADE,blank=True,null=True,default=None)
    phone = models.CharField(max_length=10,null=False,blank=False,unique=True,validators=[MinLengthValidator(10)]) #91-000-000-0000
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=4,null=True,blank=True,validators=[MinLengthValidator(4)])
    password = models.CharField(max_length=200,null=False,blank=False)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects= UserManager()
    def __str__(self):
        return self.phone

# jobs
class Jobs(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    salary = models.IntegerField(validators=[MinValueValidator(0.0)])
    num_openings = models.IntegerField(validators=[MinValueValidator(0.0)])
    requirement_level = models.TextField(max_length=2000,null=True,blank=True)
    desired_qualities = models.TextField(max_length=2000,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title + " | " + self.company.name
    
    class Meta:
        ordering = ['-created_at','-num_openings']

class Profile(models.Model):
    EDUCATION_STATUS=[
        ('AA','Associate Of Arts'),
        ('AAS','Associate Of Arts and Sciences'),
        ('AS','Associate Of Sciences'),
        ('BASc','Bachelor Of Applied Sciences'),
        ('BArch','Bachelor Of Architecture'),
        ('BA','Bachelor Of Arts'),
        ('BBA','Bachelor Of Business Administration'),
        ('BCom','Bachelor Of Arts'),
        ('BEd','Bachelor of Education'),
        ('MArch','Master of Architecture'),
        ('MA','Master Arts'),
        ('DA','Doctor Of Arts'),
        ('JD','Doctor Of Law'),
        ('MD','Doctor Of Medicine')
    ]
    GENDER_CHOICES = [
        ('M','Male'),
        ('F','Female'),
        ('O','Other')
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True)
    dob = models.CharField(max_length=10,validators=[MinLengthValidator(10)],null=True,blank=True)
    highest_education_qualification = models.CharField(choices=EDUCATION_STATUS,max_length=6,null=False,blank=False)
    city = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=200,null=True,blank=True)
    country = models.CharField(max_length=200,null=True,blank=True)
    linked_in = models.CharField(max_length=200,null=True,blank=True)
    aadhar_number = models.CharField(max_length=12,unique=True,validators=[MinLengthValidator(12)],null=True,blank=True)
    profile_photo = models.ImageField(null=True,blank=True,default="default.jpg")
    saved_jobs = models.ManyToManyField(Jobs,related_name="jobs")
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        # if self.aadhar_number and self.user.username:
        #     return self.user.username + " | " + self.aadhar_number 
        # elif self.user.username:
        #     return self.user.username
        # else:
        #     return self.aadhar_number
        return self.user.phone
    class Meta:
        ordering = ['-created']
    @property
    def imageURL(self):
        try:
            url = self.profile_photo.url 
        except:
            url = ""
        return url



class Experience(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    designation = models.CharField(max_length = 200,null=True,blank=True)
    company = models.OneToOneField(Company,on_delete=models.CASCADE)
    salary = models.IntegerField(validators=[MinValueValidator(0.0)])
    startDate = models.CharField(max_length=10,validators=[MinLengthValidator(10)],null=True,blank=True)
    endDate = models.CharField(max_length=10,validators=[MinLengthValidator(10)],null=True,blank=True)
    location = models.CharField(max_length=200,null=True,blank=True)
    role_type = models.OneToOneField(Role,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.profile.user.username + " | " + self.designation + " | " + self.company.name 

    class Meta:
        ordering = ['-created']



class Skills(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    experience = models.OneToOneField(Experience,on_delete=models.CASCADE)
    skill = models.ManyToManyField(Skill,related_name='exp_skills')
    id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True,primary_key=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.profile.user.username + " | " + self.experience.designation

    class Meta:
        ordering = ['-created']



class Applications(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True)
    job = models.ForeignKey('Jobs',on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    applied_date = models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    cv_used_bool = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job.title + " | " + self.profile.user.username

    class Meta:
        ordering = ['-created']