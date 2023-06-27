# auth/apps/user_profile/models.py
from django.conf import settings
User = settings.AUTH_USER_MODEL

from djoser.signals import  user_registered

from django.db import models


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')

    fotografia = models.ImageField(default='media/users/user_default_profile.png', upload_to='media/users/pictures',blank=True,null=True,verbose_name='Fotografia')
    telefono = models.CharField(max_length=20,blank=True,null=True,verbose_name='Telefono')
    direccion = models.CharField(max_length=200,blank=True,null=True,verbose_name='Direccion')
    dpi = models.CharField(max_length=25, blank=True,null=True)

def post_user_registered(request, user ,*args, **kwargs):
    #1. Definir usuario que ser registra
    user = user
    Profile.objects.create(user=user)

user_registered.connect(post_user_registered)