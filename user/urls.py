from django.urls import path

from .views import CutsomUserCreate,BlacklistTokenView, UserProfileView, ObtainJWTFromGoogle


app_name = 'users'

urlpatterns = [
    path('register/', CutsomUserCreate.as_view(), name ="create_user"),
    path('logout/balcklist/', BlacklistTokenView.as_view(), name ="balcklist"),
    path('profile/', UserProfileView.as_view(), name = "profile"),
    path('token/google/', ObtainJWTFromGoogle.as_view(), name='token_obtain_google'),

]