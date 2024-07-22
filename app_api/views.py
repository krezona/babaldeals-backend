from rest_framework import generics
from app.models import Product, Cart, HeroSection1,Category,Order
from .serializers import ProductSerializer,CategorySerializer, CartSerializer,CartItemSerializer, HeroSelection1Serializer, OrderSerializer, KhaltiSerializer
from rest_framework.permissions import SAFE_METHODS, BasePermission,IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from rest_framework import permissions,filters
from rest_framework.response import Response
from exception.bad_request_exception import BadRequestException
from exception.not_authorized_exception import NotAuthorized
from exception.not_found_exception import NotFound
from rest_framework import status
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
import requests
import json
from app_api import config
import paypalrestsdk
from paypalrestsdk import Payment
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.postgres.search import TrigramSimilarity
import stripe
from project import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from project import settings
from paypalrestsdk import notifications
from . import config 
from django.shortcuts import redirect
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.http import HttpResponse


from rest_framework.views import APIView, View
from django.shortcuts import get_object_or_404


from datetime import datetime

from django.views.generic import DetailView, ListView
from django.shortcuts import render,redirect



import logging

logger = logging.getLogger(__name__)

def logger_fun(request):
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")

def ProductListView(request):
    Product_List = Order.objects.all()
    context = {'product':Product_List}
    
    return render(request, 'app/product_list.html',context)
def ProductDetailView(request, pk):
    productDetail = Order.objects.get(id = pk)
    context = {'product':productDetail}
    
    return render(request, 'app/product.html',context)



class IsOwner(BasePermission):
    def has_object_permission(self, request, view,obj):
        return obj.user == request.user



class ProductList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Product.productobjects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            raise BadRequestException("enter valid data")
    def perform_create(self, serializer):
        serializer.save()
   



class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    


    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]


    def get(self, request, *args, **kwargs):
        
        try:
            return self.retrieve(request, *args, **kwargs)
        except:
            raise NotFound("No product found of this id")
        

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except:
            raise BadRequestException("enter valid data")
    
    def delete(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except:
            raise NotFound("Product not found")

class ProductFilter(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get the search query provided by the user
        search_query = self.request.query_params.get('search', None)

        # If search query is provided, filter the queryset
        if search_query:
            # Perform trigram similarity search to find closest matching words
            closest_matches = Product.objects.annotate(
                similarity=TrigramSimilarity('title', search_query)
            ).filter(similarity__gt=0.1).order_by('-similarity')

            # If no exact match found, return the closest matches
            if not queryset.exists():
                return closest_matches

        return queryset
    

    
        
    
    

class CategoryViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        try:
            queryset = Category.objects.all()
            
        except:
            raise NotFound("Category not found")  
        return queryset
    
    
                  
        


class HeroSelection1ViewSet(viewsets.ModelViewSet):
    queryset = HeroSection1.objects.all()
    serializer_class = HeroSelection1Serializer
    parser_classes = [MultiPartParser, FormParser]


    


class CartListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    



class CartDetailAPIView(generics.RetrieveAPIView):
    
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    

    def get_object(self):
        queryset = self.get_queryset()
        cart_id = self.kwargs.get("pk")
        try:
            cart = queryset.get(pk=cart_id)
        except Cart.DoesNotExist:
            raise NotFound("Cart not found.")
        
        return cart

class AddCartItemAPIView(APIView):
    permission_classes = [IsOwner]
    
    def post(self, request, pk, format=None):
        try:
            cart = Cart.objects.get(pk=pk)    
        except:
            raise NotFound("Cart not found")
        
        try: 
            self.check_object_permissions(request, cart)
        except:
            raise NotFound("Cart not founddddddd")
        
        
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            item_data = serializer.validated_data



            product_id = item_data['product_id']

            for item in cart.items:
                if item['product_id'] == product_id:
                    raise BadRequestException("Product already exists in the cart.")
            


            product = get_object_or_404(Product, pk= item_data['product_id'])

            if product.stock < item_data['quantity']:
                raise BadRequestException("Not enough stock available.")
            
            
    
            
            # product.stock -= item_data['quantity']
            # product.save()

            existing_ids = [item['id'] for item in cart.items]
            new_id = max(existing_ids, default=0) +1
            item_data['id'] = new_id
            item_data['version'] = 1
            item_data['date_created'] = str(datetime.now())
            item_data['date_updated'] = str(datetime.now())

            
            
            cart.items.append(item_data)
            cart.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise BadRequestException("enter valid data")

class UpdateCartItemAPIView(APIView):
    permission_classes = [IsOwner]
    def patch(self, request, cart_pk, item_id, format=None):
        try:
            
            cart = Cart.objects.get(pk=cart_pk)
            try:
                self.check_object_permissions(request, cart)
            except:
                raise NotFound("Cart not found")
            
        except Cart.DoesNotExist:
            raise NotFound("Cart not found.")

        item = next((item for item in cart.items if item['id'] == item_id), None)
        if not item:
            raise NotFound("Item not found in the cart.")
        
        

        
        

        item["version"] +=1
        item["date_updated"] = str(datetime.now())

        serializer = CartItemSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            # for key, value in serializer.validated_data.items():
            #     item[key] = value
            item["quantity"] = serializer.validated_data.get('quantity')
            if item["quantity"] is None:
                raise BadRequestException("Please enter the quantity value")
            
            product = get_object_or_404(Product, pk = item['product_id'])

            if product.stock < item['quantity']:
                raise BadRequestException("Not enough stock available")

            cart.save()
            return Response(item, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteCartItemAPIView(APIView):
    permission_classes = [IsOwner]
    def delete(self, request, cart_pk, item_id, format=None):
        try:
            cart = Cart.objects.get(pk=cart_pk)

            try:
                self.check_object_permissions(request, cart)
            except:
                raise NotFound("Cart not found")
        except Cart.DoesNotExist:
            raise NotFound("Cart not found.")

        item = next((item for item in cart.items if item['id'] == item_id), None)
        if not item:
            raise NotFound("Item not found in the cart.")

        # Remove the item from the items list
        cart.items.remove(item)
        cart.save()

        return Response({"detail": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class KhaltiIntentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = KhaltiSerializer

    def post(self, request,pk, *args, **kwargs):
        
        
        # retrun_url = request.data.get("return_url")
        # website_url = request.data.get("website_url")
        amount = request.data.get("amount")
        # purchase_order_id = request.data.get("purchase_order_id")
        # purchase_order_name = request.data.get("purchase_order_name")
        username = self.request.user.username
        
        
        payload = json.dumps({
            "return_url": "http://example.com/",
            "website_url": "https://example.com/",
            "amount": amount,
            "purchase_order_id": "Order1",
            "purchase_order_name": "test",
            "customer_info": {
            "name": username,
            "email": "test@khalti.com",
            "phone": "9800000001"
            }
})
        
        headers = {
            'Authorization': 'key c186931d301e4263ac43ae59e03e5324',
            'Content-Type': 'application/json',
        }
        
      
        response = requests.post('https://a.khalti.com/api/v2/epayment/initiate/', headers=headers, data=payload)
       
        response_data = response.json()
        
        
        pidx = response_data.get('pidx')
        
        
        
        # Save to database
        # khalti_instance = Khalti.objects.create(user=user, pidx=pidx, created = str(datetime.now()))

        cart= get_object_or_404(Cart, pk=pk, user = request.user)

        if not cart.items:
            raise BadRequestException("Your cart is empty")
        
        total_price = 0 
        delivery_charge = 100

        for item in cart.items:
            product = get_object_or_404(Product, pk=item['product_id'])
            if product.stock < item['quantity']:
                raise BadRequestException("Not enough stock available")
            
            
            total_price += product.price * item['quantity']
        price = total_price+delivery_charge

        if response.status_code == 200:
            order = Order.objects.create(
                    user = request.user,
                    items = cart.items,
                    price = price,
                    status = 'Pending',
                    created_at = str(datetime.now()),
                    payment_method = "Khalti",
                    payment_id = pidx,

                )
            

            
            return Response({"order_id": order.id,'pidx':pidx, "message": "Checkout initiated ."}, status=status.HTTP_201_CREATED)
        
            

        
        else:
            raise BadRequestException("error occured")
        
        # return JsonResponse({'pidx': khalti_instance.pidx}, status=201)
    
    

class CheckoutAPIView(APIView):
    

    def post(self, request, pk, format=None):

        cart= get_object_or_404(Cart, pk=pk, user = request.user)

        if not cart.items:
            raise BadRequestException("Your cart is empty")
        
        total_price = 0 
        delivery_charge = 100

        for item in cart.items:
            product = get_object_or_404(Product, pk=item['product_id'])
            if product.stock < item['quantity']:
                raise BadRequestException("Not enough stock available")
            
            
            total_price += product.price * item['quantity']
        price = total_price+delivery_charge
        payment_method = request.data.get("payment_method")
        # if payment_method not in ["cod","esewa", "khalti","paypal","stripe"]:
        #     raise BadRequestException("Unsupported payment method")
        

        if payment_method == "cod":
            order = Order.objects.create(
                    user = request.user,
                    items = cart.items,
                    price = price,
                    status = 'Accepted',
                    created_at = str(datetime.now()),
                    payment_method = "COD",
                    payment_id = "COD",


                )
            for item in cart.items:
                        product = get_object_or_404(Product, pk = item['product_id'])
                        product.stock -= item['quantity']
                        product.save()

            cart.items = []
            cart.save()

            return Response({"order_id": order.id, "message": "Checkout successful."}, status=status.HTTP_201_CREATED)
                
       
        #esewa check payment check
        elif payment_method == "esewa":
            product_code = request.data.get("product_code")
            transaction_uuid = request.data.get("transaction_uuid")
            total_amount = request.data.get("total_amount")
            if not all([product_code, transaction_uuid, total_amount]):
                raise BadRequestException("Missing transaction parameters")

            transaction_params = {
                "product_code": product_code,
                "transaction_uuid": transaction_uuid,
                "total_amount": total_amount
            }
            response = requests.get("https://uat.esewa.com.np/api/epay/transaction/status/", params=transaction_params)

            if response.status_code == 200:
                transaction_status = response.json().get("status")
                if transaction_status == "COMPLETE":
                    order = Order.objects.create(
                    user = request.user,
                    items = cart.items,
                    price = price,
                    status = 'Accepted',
                    created_at = str(datetime.now()),
                    payment_method = "Esewa",
                    payment_id = transaction_uuid,


                )
                
                    for item in cart.items:
                        product = get_object_or_404(Product, pk = item['product_id'])
                        product.stock -= item['quantity']
                        product.save()

                    cart.items = []
                    cart.save()

                    return Response({"order_id": order.id, "message": "Checkout successful."}, status=status.HTTP_201_CREATED)
                
                else:
                    raise BadRequestException("Transaction status is not complete")
                

        #khalti payment
       
        elif payment_method == "khalti":
           
            
            headers = {
                    'Authorization': 'key c186931d301e4263ac43ae59e03e5324',
                    'Content-Type': 'application/json',
            }

            pidx =  request.data.get("pidx")
            order_id = request.data.get("order_id")



            transaction_params = json.dumps({
                "pidx" : pidx,
                "order_id": order_id

            })
            
    
           

            
            response = requests.post("https://a.khalti.com/api/v2/epayment/lookup/", headers = headers, data = transaction_params)
            
            
            if response.status_code == 200:
                transaction_status = response.json().get("status")
                if transaction_status == "Completed":
                    order = get_object_or_404(Order, pk = order_id)
                    if order.payment_id == pidx:

                    
                        order.status = "Accepted"
                        order.save()
                        for item in cart.items:
                            product = get_object_or_404(Product, pk = item['product_id'])
                            product.stock -= item['quantity']
                            product.save()

                        cart.items = []
                        cart.save()
                    else:
                        raise BadRequestException("pidx doesnot match")

                    return Response({ "message": "Checkout successful."}, status=status.HTTP_201_CREATED)
                    

                    
                else:
                    raise BadRequestException("Transaction status not complete")
            else:
                raise BadRequestException("Failed to check the transaction status")
            
        elif payment_method == "paypal":
            order = Order.objects.create(
                    user = request.user,
                    items = cart.items,
                    price = price,
                    status = 'Pending',
                    created_at = str(datetime.now()),
                    payment_method = "Paypal",
                    payment_id = "id",


                )
            for item in cart.items:
                        product = get_object_or_404(Product, pk = item['product_id'])
                        product.stock -= item['quantity']
                        product.save()

            cart.items = []
            cart.save()
            
            
        elif payment_method == "stripe":
            # payment_id =  request.data.get("payment_id")
            order = Order.objects.create(
                    user = request.user,
                    items = cart.items,
                    price = price,
                    status = 'Pending',
                    created_at = str(datetime.now()),
                    payment_method = "Stripe",
                    payment_id = "id",


                )
            for item in cart.items:
                        product = get_object_or_404(Product, pk = item['product_id'])
                        product.stock -= item['quantity']
                        product.save()

            cart.items = []
            cart.save()

            return Response({"order_id": order.id, "message": "Checkout initiated."}, status=status.HTTP_201_CREATED)
        


        elif payment_method == "connectips":
            order = Order.objects.create(
                    user = request.user,
                    items = cart.items,
                    price = price,
                    status = 'Pending',
                    created_at = str(datetime.now()),
                    payment_method = "ConnectIps",
                    payment_id = "id",


                )
            for item in cart.items:
                        product = get_object_or_404(Product, pk = item['product_id'])
                        product.stock -= item['quantity']
                        product.save()

            cart.items = []
            cart.save()


            
            

@method_decorator(csrf_exempt, name="dispatch")
class ProcessWebhookViewPAYPAL(View):
    def post(self, request):
        if "HTTP_PAYPAL_TRANSMISSION_ID" not in request.META:
            return HttpResponseBadRequest()
        
        

        auth_algo = request.META['HTTP_PAYPAL_AUTH_ALGO']
        cert_url = request.META['HTTP_PAYPAL_CERT_URL']
        transmission_id = request.META['HTTP_PAYPAL_TRANSMISSION_ID']
        transmission_sig = request.META['HTTP_PAYPAL_TRANSMISSION_SIG']
        transmission_time = request.META['HTTP_PAYPAL_TRANSMISSION_TIME']
        webhook_id = settings.PAYPAL_WEBHOOK_ID
        event_body = request.body.decode(request.encoding or "utf-8")

        


        valid = notifications.WebhookEvent.verify(
            transmission_id=transmission_id,
            timestamp=transmission_time,
            webhook_id=webhook_id,
            event_body=event_body,
            cert_url=cert_url,
            actual_sig=transmission_sig,
            auth_algo=auth_algo,
        )

        if not valid:
            return HttpResponseBadRequest()
        
        webhook_event = json.loads(event_body)
       
       # print(webhook_event)
        event_type = webhook_event["event_type"]

        CHECKOUT_ORDER_APPROVED = "PAYMENT.SALE.COMPLETED"

        if event_type == CHECKOUT_ORDER_APPROVED:
            
            payment_id=webhook_event["resource"]["parent_payment"]
            print(f'payment id: {payment_id}')
            #logic here

            try:
             order=Order.objects.get(id=payment_id, payment_method='paypal')
             order.status = "Accepted"
             order.save()
            except:
                raise BadRequestException("no such payment intented")
            
         
        return HttpResponse()
    

        
from rest_framework.decorators import api_view

@csrf_exempt
@api_view(['POST'])
def create_payment_intent(request):
    
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        request_data = json.loads(request.body)

        try:
           
            total_amount = request_data.get('total_amount')
            pk = request_data.get('order_id')
            

            intent = stripe.PaymentIntent.create(
                amount=total_amount * 100,  # in cents
                currency='usd',
                payment_method_types=['card'],
                description='babaldeals payment',
            )
            

           

            order = get_object_or_404(Order, pk = pk)
            order.payment_id = intent.client_secret.split('_secret')[0]
            order.save()

            return JsonResponse({
                "sessionId":intent.client_secret,
                'Access-Control-Allow-Origin':'*'
                
                
               
            }, status=200)




        except Exception as e:
            # Handle any errors and return an error response
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # If the request method is not POST, return a method not allowed response
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    





@csrf_exempt
def stripe_webhook(request):

    event=json.loads(request.body)

    
    
    if event['type']=='charge.succeeded' and event["data"]["object"]["status"]=="succeeded":

        try:
         
         instance=Order.objects.get(payment_id=event["data"]["object"]["payment_intent"])
         instance.status="Accepted"
         instance.save()


        
        
        except Order.DoesNotExist:
            return JsonResponse ({"message":"No such intent made"}, status=404)
        
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=400)
        
       
    return HttpResponse()

import hashlib
import base64
class ConnectIps(APIView):
    def post(self, request, *args, **kwargs):

        merchant_id = 3049
        app_id = "MER-3049-APP-1"
        app_name = "Kerzona"
        txn_id = "txnId"
        txn_date = "dare"
        txn_currency = "nrs"
        txn_amount = 10000
        reference_id = "iddd"
        remarks = "hello world"
        particulars = "asdasd"

        token_string = f"MERCHANTID={merchant_id},APPID={app_id},APPNAME={app_name},TXNID={txn_id},TXNDATE={txn_date},TXNCRNCY={txn_currency},TXNAMT={txn_amount},REFERENCEID={reference_id},REMARKS={remarks},PARTICULARS={particulars},TOKEN = TOKEN"
    
        
  
        hashed_token = hashlib.sha256(token_string.encode()).digest()

       
        signature = base64.b64encode(hashed_token).decode()

        

    

        

        
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

        
class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)

    def get_object(self):
        
        queryset = self.get_queryset()
        order_id = self.kwargs.get('pk')
        try:
            order = queryset.get(pk = order_id)
        except:
            raise NotFound("Order id not found")
        return order
    









