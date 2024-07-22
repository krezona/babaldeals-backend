from django.urls import path,include
from .views import ProductList, ProductDetail,ProductFilter, CategoryViewset
from rest_framework.routers import DefaultRouter
# from .views import PaypalValidatePaymentView, PaypalPaymentView
from .views import CartListCreateAPIView, CartDetailAPIView,AddCartItemAPIView,UpdateCartItemAPIView,DeleteCartItemAPIView, CheckoutAPIView, OrderDetailAPIView, OrderListAPIView,KhaltiIntentView,ProcessWebhookViewPAYPAL

app_name= 'app_api'
# from .views import CreateStripeCheckoutSessionView
from .views import create_payment_intent



router = DefaultRouter()
# router.register(r'hero1', HeroSelection1ViewSet)
router.register(r'category', CategoryViewset, basename='category')

from .views import ProductDetailView, ProductListView
from . import views

urlpatterns = [ 
    # path('category/',CategoryList.as_view(), name= 'category'),
    path('', include(router.urls)),
    path("pv/", views.ProductListView, name="product-list"),
    path("pv/<int:pk>/", views.ProductDetailView, name="productD"),
    path('products/<int:pk>/', ProductDetail.as_view(),name='product-detail'),
    path('products/', ProductList.as_view(),name= "listcreate"),
    path('search/custom/', ProductFilter.as_view(),name= "product-search"),
    path('carts/', CartListCreateAPIView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('carts/<int:pk>/add-item/', AddCartItemAPIView.as_view(), name='add-cart-item'),
    path('carts/<int:cart_pk>/items/<int:item_id>/', UpdateCartItemAPIView.as_view(), name='update-cart-item'),
    path('carts/<int:cart_pk>/items/<int:item_id>/delete/', DeleteCartItemAPIView.as_view(), name='delete-cart-item'),
    path('carts/<int:pk>/checkout/',CheckoutAPIView.as_view(),name = 'cart-checkout' ),
    path('khalti/intent/<int:pk>/',KhaltiIntentView.as_view(), name = 'khalti' ),
   
    path('stripe-intent/', create_payment_intent, name= 'create_payment_intent'),
    path('api/paypal/webhook/', ProcessWebhookViewPAYPAL.as_view(), name='paypal-webhook'),
    path('orders/',OrderListAPIView.as_view(),name = 'order-list'),
    path('order/<int:pk>/',OrderDetailAPIView.as_view(),name = 'order-detail'),
    
    
]

    