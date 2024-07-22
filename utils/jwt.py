# utils/jwt.py

from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import Token


def jwt_payload_handler(user, sociallogin=None):
    """
    Custom payload handler to include additional user information in JWT
    when logging in with Google via django-allauth
    """
    payload = {
        'user_id': user.id,
        'email': user.email,
        'username': user.username,
        'exp': timezone.now() + timedelta(minutes=60)  # Token expiration
    }

    # Optionally, add additional claims based on your needs
    if sociallogin:
        payload['provider'] = sociallogin.account.provider
        # Add more custom claims as needed from social account

    return payload
