from django.urls import path, include
from .views import AccountProfile, UpdateProfile, auth_code


urlpatterns = [
  path('', include('allauth.urls')),
  path('profile/', AccountProfile.as_view(), name='account_profile'),
  path('account_edit/', UpdateProfile.as_view(), name='account_edit'),
  path('auth_code/', auth_code, name='auth_code')
]
