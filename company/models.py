from django.db import models
import uuid 
from django.core.validators import MinValueValidator,MinLengthValidator,MaxLengthValidator
# Create your models here.
# Company model
class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True)
    name =models.CharField(max_length=200,null=False,blank=False,unique=True)
    address = models.TextField(max_length=600,null=True,blank=True,unique=True)
    industry = models.CharField(max_length=200,null=True,blank=True)
    company_logo_url = models.ImageField(null=True,blank=True,default="defaultCompany.jpg")
    number_of_employees = models.IntegerField(validators=[MinValueValidator(0.0)])
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    @property
    def imageURL(self):
        try:
            url = self.profile_photo.url 
        except:
            url = ""
        return url

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created','-updated']

# role model
class Role(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created','-updated']

class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    sector = models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name + " | " + self.sector 

    class Meta:
        ordering = ['-created','-updated']
