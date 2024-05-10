from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CreateUser, OtpUnit, JwtUnit


urlpatterns = [

    path('api/register', CreateUser.as_view(), name='user_register'),

    path('api/otp/create', OtpUnit.as_view(), name='otp_create'),

    path('api/token', JwtUnit.as_view(), name='token_create'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # path('api/otp/verify', CreateUser.as_view()),

    # path('', include('djoser.urls.jwt')),
]
