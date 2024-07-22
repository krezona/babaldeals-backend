from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _






#image upload
def upload_to(instance,filename):
    return 'products/{filename}'.format(filename = filename)


#first hero section
class HeroSection1(models.Model):
    title= models.CharField(max_length=200)
    heading = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
    
class HeroImage1(models.Model):
    hero_section = models.ForeignKey(HeroSection1, related_name='herofirstimages',on_delete=models.CASCADE)
    image = models.ImageField(_('Image'), upload_to= upload_to, default='products/default.jpg')

    def __str__(self):
        return str(self.image)
    



#category
class Category(models.Model):
    name = models.CharField(max_length =100)


    def __str__(self):
        return self.name
    

#products
class Product(models.Model):


    class ProductObjects(models.Manager):
        
        def get_queryset(self):
            return super().get_queryset() .filter(status='available')

    options = (
        ('outofstock', 'Out of Stock'),
        ('available', 'Available'),
    )

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1
    )
    title = models.CharField(max_length = 250)
    image = models.ImageField(_('Image'), upload_to= upload_to, default='products/default.jpg')
    description = models.TextField(null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length= 250 , unique= True)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=options, default='available')
    objects = models.Manager() #default manager
    productobjects = ProductObjects() # custom manager

    def __str__(self):
        return self.title
    





class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.JSONField(default = list)


    def __str__(self):
        return f'Cart {self.id} for {self.user.username}'
    

ORDER_STATUS = (
    ('Accepted', 'Accepted'),
    ('Pending', 'Pending'),
    ('Failed', 'Failed'),
)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    items = models.JSONField(default = list)
    price = models.CharField()
    created_at = models.CharField()
    status = models.CharField(max_length=50, choices= ORDER_STATUS, default='Pending')
    payment_method = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    






    
    