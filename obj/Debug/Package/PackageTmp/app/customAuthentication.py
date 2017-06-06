from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from .models import User

class MyBackEnd(ModelBackend):
    def authenticate(self, **credientials):
        return 'username' in credientials and self.authenticate_by_is_authorized(**credientials)

    def authenticate_by_is_authorized(self, username=None, password=None):
         try:
             user = User.objects.get_by_natural_key(username=username)
         except User.DoesNotExist:
             user = None
         
         if user:
            return user if user.is_authorized and user.check_password(password) else None
         else:
            return none    
