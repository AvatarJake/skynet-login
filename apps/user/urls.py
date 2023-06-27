from django.urls import path

from .views import *
from .views import * 

urlpatterns = [
    # path('users/',UserView.as_view(),name='user_list'),
    # path('users/<str:id>',UserView.as_view(),name='user_process'),
    # path('users/<str:id>/change/',UserView.as_view(),name='user_puts'),
    
    path('list/', ListAllUsersView.as_view()),
    path('get/<id>/', GetUserView.as_view()),
    path('get/profile/<slug>', GetUserProfileView.as_view()),
    path('get_details/<id>/', GetUserDetailsView.as_view()),
    path('auth/users/me/update/', UpdateProfileView.as_view(), name='update-profile'),
]