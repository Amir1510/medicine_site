
from django.db import models
from django.contrib.auth.hashers import make_password
from dirtyfields import  DirtyFieldsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CreateUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CreateUser(DirtyFieldsMixin, AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CreateUserManager() 

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk or 'password' in self.get_dirty_fields():
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    
class Plan(models.Model):
    BLODD_CHOICES = [
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ("B-", 'B-'),
        ("AB+", 'AB+'),
        ("AB-", 'AB-'),
    ]
    AGE_CHOICES = [(str(i), f"{i} лет") for i in range(0, 100)]
    HEIGHT_CHOICES = [(str(i), f"{i} см") for i in range(80, 201)]
    WEIGHT_CHOICES = [(str(i), f"{i} кг") for i in range(10, 201)]
    username = models.CharField(max_length=20, unique=True, default='default_username')
    weight = models.CharField(choices=WEIGHT_CHOICES, default='10')
    group_of_blood = models.CharField(max_length=10, choices=BLODD_CHOICES, default='0+')
    height = models.CharField(max_length=10, choices=HEIGHT_CHOICES, default='80')
    age = models.CharField(max_length=10, choices=AGE_CHOICES, default='0')

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.OneToOneField(
        Plan, on_delete=models.CASCADE, to_field='username', related_name='data'
    )
    data = models.CharField(max_length=20)
    time = models.CharField(default='8:30')

  

class BloodGroup(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, verbose_name="Группа крови")
    is_active = models.BooleanField(default=False, verbose_name="Состояние")

    def __str__(self):
        return f"{self.group} - {'Состояние' if self.is_active else 'Состояние'}"
    
