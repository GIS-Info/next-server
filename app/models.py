from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class UserInfo(AbstractUser):
    mobile = models.CharField(validators=[RegexValidator(regex=r"^\+?1?\d{8,15}$")], max_length=16, unique=True,
        verbose_name="电话号码", null=True, blank=True)
    class Meta:
        verbose_name_plural = verbose_name = '用户信息'
