
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.views import CookieTokenObtainPairView, ProtectedView
from django.conf.urls import handler404
from app_api.views import stripe_webhook
# from app_api.views import custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls',namespace='app')),
    path('api/',include('app_api.urls', namespace='app_api')),
    path('api/user/',include('user.urls', namespace='user')),
   
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/', include('allauth.urls')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', CookieTokenObtainPairView.as_view(), name='cookie_token_obtain_pair'),
    path('api/protected/', ProtectedView.as_view(), name='protected_view'),
    path('webhooks/stripe/', stripe_webhook, name = "stripe-webhook"),
   
    
    


]
# handler404 = custom_404_view
