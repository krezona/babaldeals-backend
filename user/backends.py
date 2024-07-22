from django.contrib.auth.backends import ModelBackend , BaseBackend
from .models import myUser



class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Allow login with email or phone number
        try:
            user = myUser.objects.get(email=username)
        except myUser.DoesNotExist:
            try:
                user = myUser.objects.get(phone_number=username)  # Assuming phone number is stored in a profile related model
            except myUser.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return myUser.objects.get(pk=user_id)
        except myUser.DoesNotExist:
            return None

# class EmailOrPhoneBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         user = None
#         if username:
#             try:
#                 if '@' in username:
#                     user = myUser.objects.get(email=username)
#                 else:
#                     user = myUser.objects.get(phone_number=username)
#             except myUser.DoesNotExist:
#                 return None

#             if user and user.check_password(password) and self.user_can_authenticate(user):
#                 return user
#         return None

#     def get_user(self, user_id):
#         try:
#             return myUser.objects.get(pk=user_id)
#         except myUser.DoesNotExist:
#             return None