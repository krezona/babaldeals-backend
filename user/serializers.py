from rest_framework import serializers
from .models import myUser

from exception.bad_request_exception import BadRequestException




class RegisterUserSerializer(serializers.ModelSerializer):
    

    email_or_phone = serializers.CharField(write_only=True)
    class Meta:
         model = myUser
         fields = [ 'username', 'password', 'first_name', 'last_name','email', 'phone_number','email_or_phone']
         extra_kwargs = {'password':{'write_only':True}}


    def validate(self, attrs):
          email_or_phone =attrs.get('email_or_phone')
          
         
          
          if '@' in email_or_phone:
               if myUser.objects.filter(email = email_or_phone).exists():
                   raise BadRequestException("Email already exists")
               attrs['email'] = email_or_phone
               attrs['phone_number'] = None
          else:
               if myUser.objects.filter(phone_number = email_or_phone).exists():
                   raise BadRequestException("Phone number already exists")
               attrs['phone_number'] = email_or_phone
               attrs['email'] = None

     
          return attrs
    


    def create(self, validated_data):
         email_or_phone = validated_data.pop('email_or_phone')
         password = validated_data.pop('password', None)
         
         instance = self.Meta.model(**validated_data)

         if '@' in email_or_phone:
            validated_data['email'] = email_or_phone
            
         else:
            validated_data['number'] = email_or_phone
            
         
         if password is not None:
            instance.set_password(password)
            instance.save()
            return instance      
          
class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = myUser
        fields = [ 'profile','username','first_name', 'middle_name','last_name','email','address','phone_number']
        
    
    def validate(self, attrs): 
       email = attrs.get('email')
       phone_number = attrs.get('phone_number')

       if not email and not phone_number:
           raise BadRequestException("at least one of email or phone number must be there") 
       
       return attrs
         



