from rest_framework import serializers
from app.models import Product,  HeroImage1, HeroSection1, Cart,Category,Order
from exception.bad_request_exception import BadRequestException
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Max
import pytz




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','title','category','image','description', 'price','slug','stock','status')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','id']
    def validate(self, attrs):
        name = attrs.get('name')
        

        if name:
            existing_category = Category.objects.filter(name__iexact=name).exists()
            if existing_category:
                raise BadRequestException("Category already exists")
        return attrs
        
            




class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroImage1
        fields = ('id','image')

class HeroSelection1Serializer(serializers.ModelSerializer):
    herofirstimages = HeroImageSerializer(many=True, read_only=True)
    class Meta:
        model = HeroSection1
        fields = ['title', 'heading', 'description','herofirstimages']


class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(default =1)
    product_id = serializers.IntegerField()    
    version = serializers.IntegerField(default = 1)
    quantity = serializers.IntegerField()
    date_created = serializers.CharField(default = str(datetime.now()))
    date_updated = serializers.CharField(default = str(datetime.now()))
    

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        if quantity == 0:
            raise BadRequestException("The quantity cannot be 0")
        return attrs
        
    def validate_product_id(self, value):
        try:
            product = Product.objects.get(pk=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return value

    
            

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product = Product.objects.get(id=representation['product_id'])
        representation['product'] = ProductSerializer(product).data
        return representation
    
    
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only= True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']
        read_only_fields = ['user','items']

   

    def create(self, validated_data):

        # validated_data['user'] = self.context['request'].user
        user = self.context['request'].user
        if Cart.objects.filter(user=user).exists():
            raise BadRequestException("A user can only have one cart")



        cart = Cart.objects.create(user= user, **validated_data)
        return cart

class KhaltiSerializer(serializers.ModelSerializer):
    class Meta:
        
        fields = ['user', 'pidx', 'created']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'price', 'created_at', 'status']

    


    
    


    
 