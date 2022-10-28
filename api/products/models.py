from django.db import models
from api.users.models import *
# Create your models here.

def upload_path(instance ,filename):
    return '/'.join(['images',str(instance.id),filename]) 

class Product(models.Model):
    image = models.ImageField(
        upload_to = upload_path,
        null = False
    )
    seller = models.ForeignKey(
        CustomUser,
        null = False,
        on_delete = models.CASCADE
    )
    name = models.CharField(
        max_length = 100,
        null = False
    )
    short_describtion = models.CharField(
        max_length = 100,
        null = True,
        blank =True
    )
    describtion = models.CharField(
        max_length = 100,
        null = True,
        blank =True
    )
    price = models.IntegerField(
        null = False,
        blank = False
    )
    discount = models.IntegerField(
        default = 0,
        null = False,
        blank = False
    )
    final_price = models.IntegerField(
        default = 0,
        null = True,
        blank = True
    )
    is_available = models.BooleanField(
        null = True
    )
    created_on = models.DateTimeField(
        auto_now_add = True
        # default =''
    )

    def save(self, *args, **kwargs):
        self.final_price = self.price - self.discount 
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}" + "|" + f"{self.seller.first_name}"