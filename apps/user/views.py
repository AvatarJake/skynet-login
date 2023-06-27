from rest_framework_api.views import StandardAPIView
import json, uuid
from rest_framework import serializers
from rest_framework import permissions
from .serializers import UserSerializer
from django.http import JsonResponse
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt
from apps.profile.serializers import UserProfileSerializer
from apps.profile.models import Profile
from django.db import models
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json
import uuid

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
    
class ListAllUsersView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        user_data = UserSerializer(users, many=True).data
        return self.paginate_response(request, json.dumps(user_data, cls=UUIDEncoder))
    

class GetUserView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id, *args, **kwargs):
        cache_key = f'user_{id}'
        user_data = cache.get(cache_key)

        if not user_data:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user).data
            user_data = serializer
            cache.set(cache_key, user_data, 60 * 15)  # Cache for 15 minutes

        return self.send_response(user_data)
    

class GetUserProfileView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, slug, *args, **kwargs):
        print(slug)
        return self.send_response('profile_data')


class GetUserProfileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='user.id')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    slug = serializers.CharField(source='user.slug')
    verified = serializers.BooleanField(source='user.verified')
    picture = serializers.ImageField(source='user.profile.picture')

    is_online = serializers.BooleanField(source='user.is_online')
    
    class Meta:
        model = Profile
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'slug', 'verified', 'picture', 'is_online']
    
class GetUserDetailsView(StandardAPIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    permission_classes = (permissions.AllowAny,)
    def get(self, request, id, *args, **kwargs):
        user = User.objects.prefetch_related('profile', 'wallet').get(id=id)
        serializer = UserProfileSerializer(user.profile)
        return self.send_response(serializer.data)
    
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def put(self, request, id=None):
        jd = json.loads(request.body)
        if id:
            try:
                uuid_obj = uuid.UUID(id)
                user = User.objects.filter(id=str(uuid_obj)).first()
                if user:
                    user.email = jd.get('email', user.email)
                    user.username = jd.get('username', user.username)
                    user.first_name = jd.get('first_name', user.first_name)
                    user.last_name = jd.get('last_name', user.last_name)
                    user.fecha_nacimiento = jd.get('fecha_nacimiento',user.fecha_nacimiento)
                    user.dpi = jd.get('dpi', user.dpi)
                    user.fecha_contratacion = jd.get('fecha_contratacion',user.fecha_contratacion)
                    user.supervisor = jd.get('supervisor', user.supervisor)
                    user.is_active=jd.get('is_active',user.is_active)
                    user.is_online = jd.get('is_online', user.is_online)
                    user.is_staff = jd.get('is_staff', user.is_staff)
                    user.role = jd.get('role', user.role)
                    user.save()
                    datos = {'message': "Usuario actualizado correctamente"}
                else:
                    datos = {'message': "Usuario no encontrado"}
            except ValueError:
                datos = {'message': "Formato de UUID no válido"}
        else:
            users = list(User.objects.values())
            if len(users) > 0:
                datos = {'message': "Éxito", 'users': users}
            else:
                datos = {'message': "No se encontró información"}

        return JsonResponse(datos)