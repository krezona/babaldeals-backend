from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.core.validators import validate_slug
from rest_framework import generics
from exception.bad_request_exception import BadRequestException
from .models import myUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter



class CutsomUserCreate(APIView):
    permission_classes  = [AllowAny]


    def post(self,request):
        reg_serializer = RegisterUserSerializer(data = request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()

            if newuser:
                return Response(status = status.HTTP_201_CREATED)
        return Response(reg_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    


class CookieTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):

        username = request.data.get("username") or request.data.get("phone_number")
        password = request.data.get("password")
        
        # if not username or not password: 
        #     # raise BadRequestException("Invalid request, field might be missing")
        #     raise Exception("Internal Server Errorsss")
        user = authenticate(username=username ,password=password)

        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)




            #return jwt in response

            # response = JsonResponse({
            #     "refresh": refresh_token,
            #     "access": access_token,
            # })
            response = JsonResponse({"success": "Logged in successfully"})

             #Setting the cookie for refresh token


            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value = refresh_token,
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                httponly=True,
                secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
                samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax'),


            )
            
            # Setting the cookie for access token
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                httponly=True,
                secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
                samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax'),
            )
            return response
        

        else:
        
        
            raise BadRequestException("Enter valid data!")

        #    except CustomException as e:
        #        response = custom_exception_handler(e, {})
        #    return response
            
            # return JsonResponse({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        

        
        

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view!"})
    


class ObtainJWTFromGoogle(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Handle the incoming Google access token
        access_token = request.data.get('access_token')

        # Obtain the token from the GoogleOAuth2Adapter
        adapter = GoogleOAuth2Adapter()
        user = adapter.authenticate(request, access_token)

        if user:
            # Generate JWT token for the user
            tokens = self.get_tokens_for_user(user)
            return Response({
                'access': str(tokens.access_token),
                'refresh': str(tokens.refresh_token),
            })

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    

   
    

class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except:
            raise BadRequestException("This is a bad request")
        

        
class UserProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = myUser.objects.filter()


    def get_object(self):
        return self.request.user
        






