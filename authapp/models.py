from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(verbose_name='email',max_length=255,unique=True)
    phone = models.CharField(null=True,max_length=255)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']
    # REQUIRED_FIELDS = ['username','phone','first_name','last_name']
    # Add Fields in Database
    USERNAME_FIELD = 'username'

    def get_username(self):
        return self.email