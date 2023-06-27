from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from slugify import slugify
import uuid
import re

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        def create_slug(username):
            pattern_special_characters = r'\badmin\b|[!@#$%^~&*()_+-=[]{}|;:",.<>/?]|\s'
            if re.search(pattern_special_characters, username):
                raise ValueError('El usuario contiene caracteres inválidos')
            username = re.sub(pattern_special_characters, '', username)
            return slugify(username)
        
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
        
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.role = "Admin"
        user.verified = True
        user.save(using=self._db)
        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    roles = (
        ('administrador', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('tecnico', 'Tecnico'),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True, blank=True)
    dpi = models.CharField(max_length=100,blank=True, null=True)
    fecha_contratacion = models.DateField('Fecha de Contratacion', null=True, blank=True)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    role = models.CharField(max_length=100, choices=roles, default='Tecnico')
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']


    def __str__(self):
        return self.email
