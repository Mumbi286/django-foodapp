from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .managers import ItemManager
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['user_name','item_price']),
        ]


    def __str__(self):
        return self.item_name + ":" + str(self.item_price)
    
    def get_absolute_url(self):
        return reverse('myapp:index')
    
    # overriding the delete method in views.py
    def delete(self,using=None,keep_parents=False):
        self.is_deleted = True 
        self.deleted_at = timezone.now()
        self.save()

    

    user_name = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    item_name = models.CharField(max_length=200,db_index=True)
    item_desc = models.CharField(max_length=10000)
    item_price = models.DecimalField(max_digits=6, decimal_places=2,db_index=True)
    item_image = models.URLField(max_length=500, default='https://img.magnific.com/premium-psd/pizza-slices-burgers-floating-isolated-transparent-background-rounded-by-spices-food_1232930-3777.jpg?semt=ais_hybrid&w=740&q=80')
    is_available = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)

    # soft deleting  flag 
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True) # saves timesstamp when deleted 


    objects = ItemManager()
    all_objects = models.Manager()


class Category(models.Model):
    name = models.CharField(max_length=100)
    added_on = models.DateField(auto_now=True)
    def __str__(self):
        return self.name
