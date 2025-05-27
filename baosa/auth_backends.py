# auth_backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, request, name=None, contact=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(name=name, contact=contact)
            # Auto-generated password is contact+name
            if user.check_password(f"{contact}{name}"):
                return user
        except UserModel.DoesNotExist:
            return None