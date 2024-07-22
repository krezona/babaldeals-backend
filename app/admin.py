from django.contrib import admin
from . import models
from django import forms
from django_json_widget.widgets import JSONEditorWidget




@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'price','description','image','stock','status', 'slug',)
    prepopulated_field = {'slug': ('title',),}

@admin.register(models.Category)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' )
    

class CartAdminForm(forms.ModelForm):
    class Meta:
        model = models.Cart
        fields = '__all__'
        widgets = {
            'items': JSONEditorWidget(),
        }
        
@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    form = CartAdminForm
    list_display = ('id', 'user', 'get_items')
    search_fields = ('user__username',)
    list_filter = ('user',)

    def get_items(self, obj):
        return len(obj.items)
    get_items.short_description = 'Number of Items'


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = '__all__'
        widgets = {
            'items' : JSONEditorWidget(),
        }

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_items', 'price', 'created_at', 'status','payment_method','payment_id', )

    def get_items(self, obj):
        return len(obj.items)
    get_items.short_description = 'Total Items'
    



admin.site.register(models.HeroSection1)
@admin.register(models.HeroImage1)
class HeroIMage1Admin(admin.ModelAdmin):
    list_display = ['id', 'image']