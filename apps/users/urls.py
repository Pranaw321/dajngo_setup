from django.urls import path, include
from .views import *
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenVerifyView,)

urlpatterns = [ 
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/register', views.RegisterAPI.as_view()),
    path('api/auth/login', views.LoginAPI.as_view()),
    path('api/auth/user', views.UserAPI.as_view()),    

]
