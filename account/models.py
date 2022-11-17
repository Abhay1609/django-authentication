from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken





class UserManager(BaseUserManager):
    def create_user(self,roll_no,email, full_name ,branch ,year, gender,mobile_number, password=None,password2=None):
        """
        Creates and saves a User with the given email, name ,tc and password.
        """
        if not roll_no:
            raise ValueError('Users must have a Roll number.')
        if not email:
            raise ValueError('Users must have a Email.')

        user = self.model(
            roll_no=roll_no,
            email=self.normalize_email(email),
            full_name=full_name,
            branch=branch,
            gender=gender,
            mobile_number=mobile_number,
            year=year
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,roll_no, email,year, full_name  ,branch , gender,mobile_number, password=None):
        """
        Creates and saves a superuser with the given email, name , tc and password.
        """
        if not roll_no:
            raise ValueError('Users must have a Roll number.')
        if not email:
            raise ValueError('Users must have a Email.')
        user = self.create_user(
            roll_no,
            password=password,
            email=email,
            full_name=full_name,

            branch=branch,
            gender=gender,
            mobile_number=mobile_number,
            year=year
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    full_name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True)
    roll_no=models.CharField(max_length=14,unique=True,null=False,blank=False)
    mobile_number=models.CharField(max_length=10,null=True)
    year=models.CharField(max_length=3)
    branch=models.CharField(max_length=10,null=True)
    gender=models.CharField(max_length=10,null=True)
    isverified=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password2=models.CharField(max_length=40)



    objects=UserManager()


    USERNAME_FIELD='roll_no'
    REQUIRED_FIELDS= ['email','full_name','year','gender','mobile_number','branch']

    def __str__(self):
        return self.roll_no

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access':str(refresh.access_token)
        }


# Create your models here.