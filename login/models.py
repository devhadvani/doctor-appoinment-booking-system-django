from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
   
class Custom(AbstractUser):
    first_name = models.CharField(max_length=30,blank=True)
    last_name = models.CharField(max_length=30,blank=True)
    # imag = models.CharField(max_length=30,blank=True)
    image = models.ImageField(upload_to="images", null = True, blank=True)
    email = models.EmailField(max_length=100,unique=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    address = models.CharField(blank=True, max_length=300)
    city = models.CharField(max_length=30,blank=True)
    state = models.CharField(max_length=30,blank=True)
    pin = models.IntegerField(blank=True,default=0)
    role =(
        ('is_doctor','doctor' ),
        ('is_patient','patient')
        )
    roles = models.CharField(max_length=10, choices=role,default=is_doctor)

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        

        user = self.model(
            email=self.normalize_email(email)
        )
        USERNAME_FIELD ="email"
        user.set_password(password)
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user
    
    

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Blog(models.Model):
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null = True)
    image = models.ImageField(upload_to="images", null = True, blank=True)
    title = models.CharField(max_length=70)
    summary = models.TextField()
    description = models.TextField()
    draft = models.BooleanField(default=False)

class Book(models.Model):
    require = models.CharField(max_length=200,null=True)
    description = models.TextField()
    start_time = models.DateField()
    end_time = models.TimeField()