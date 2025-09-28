import os
import uuid
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=15, blank=False ,null=False , unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


def _get_avatar_path(obj , filename):
    now = timezone.now()
    base_path = "avatars"
    new_filename = uuid.uuid4()
    # uuid v4 not need anything and uuid.NAME_SPACE  not important
    ext = os.path.splitext(filename)[1]
    p  = os.path.join(base_path, now.strftime('%y/%m'), f'{new_filename}{ext}')
    return p



class Profile(models.Model):
    user = models.OneToOneField('User',on_delete=models.CASCADE,related_name="profile")
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to=_get_avatar_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return f"Profile of {self.user.email}"


class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    blocked = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def is_blocked(self):
        if self.blocked and timezone.now() < self.blocked:
            return True
        return False

class PasswordReset(models.Model):
    user = models.OneToOneField('User',on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)


    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
