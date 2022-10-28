from django.contrib.auth import get_user_model, authenticate
from django.http import HttpRequest
from django.contrib.auth.backends import BaseBackend
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings

class MyCustomAuthBackend(BaseBackend):
    """
    Custom Email Backend to perform authentication via email and phone
    """
    def authenticate(self, request,username, password):
         print(username,password)
         my_user_model = get_user_model()
         try:
            user = my_user_model.objects.get(username=username.lower())
            if user.check_password(password):
                return user # return user on valid credentials
         except my_user_model.DoesNotExist:
            return None # return None if custom user model does not exist 
         except:
            return None # return None in case of other exceptions

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None

