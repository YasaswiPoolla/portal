from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.base_user import AbstractBaseUser
from trip_project.trip_app.model_managers import UserManager

# Create your models here.
class User(AbstractBaseUser):
    objects = UserManager()
    user_sqn = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50, db_column="firstname")
    last_name = models.CharField(max_length=50, db_column="lastname")
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20, db_column="mobile")
    last_login = models.DateTimeField(db_column="last_login", auto_now_add=True)
    is_active = models.BooleanField(default=False, db_column="isActive")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class UserException(models.Model):
    exception_sqn = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, db_column="user_sqn", null=True)
    user_request = JSONField()
    stack_trace = models.TextField()
    log_datetime = models.DateTimeField(db_column="logDateTime", auto_now_add=True)
    status = models.BooleanField(default=False)