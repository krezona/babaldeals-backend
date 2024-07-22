from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, middle_name, last_name, address, phone_number, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name,middle_name, last_name, address, phone_number, password, **other_fields)

    def create_user(self, email, username, first_name,middle_name, last_name, address, phone_number, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name,middle_name = middle_name,
                            last_name = last_name, address = address, phone_number = phone_number, **other_fields)
        user.set_password(password)
        user.save()
        return user
    

    
    
#user profile picture
def upload_to(instance,filename):
    return 'profile_picture/{filename}'.format(filename = filename)


class myUser(AbstractBaseUser, PermissionsMixin):

    profile = models.ImageField(_('Image'), upload_to= upload_to, default='profile_picture/default.jpg')
    email = models.EmailField(_('email address'), unique=True, blank=True, null= True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=False)
    phone_number = models.CharField(max_length=10, blank=True,unique=True, null=True)
    address = models.CharField(max_length=100, blank = True)
    start_date = models.DateTimeField(default=timezone.now)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email' or 'phone_number'
    REQUIRED_FIELDS = ['username', 'first_name', 'middle_name', 'last_name', 'address','phone_number']

    def __str__(self):
        return self.username





