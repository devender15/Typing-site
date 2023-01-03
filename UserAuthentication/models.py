from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from Room.models import Room


# Create your models here.

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _creat_user(self, email, password, is_superuser, is_staff, **extra_fields):

        if(not email):
            raise ValueError('Users must have an email address')

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, is_superuser, is_staff, **extra_fields):
        return self._creat_user(email, password, is_superuser, is_staff, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._creat_user(email, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=254, unique=True)
    fname = models.CharField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    board = models.CharField(max_length=100, default='CBSE', null=True, unique=False)
    grade = models.CharField(max_length=20, null=True)
    institute = models.CharField(max_length=500, unique=False, blank=True)
    approved = models.BooleanField(default=False, null=True, blank=True)
    room  = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    website_url = models.CharField(max_length=100, null=True, blank=True)
    instagram_url = models.CharField(max_length=100, null=True, blank=True)
    facebook_url = models.CharField(max_length=100, null=True, blank=True)
    telegram_url = models.CharField(max_length=100, null=True, blank=True)
    youtube_url = models.CharField(max_length=100, null=True, blank=True)


    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def get_absolute_url(self):
        return "/users/%i" % (self.pk)

