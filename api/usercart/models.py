from django.db import models
from api.models import *
# Create your models here.

class UserCart(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField(
        Product,
    )
    created_at = models.DateTimeField(
        auto_now_add = True
    )
    edited_at = models.DateField(
        auto_now_add = True
    )

    def __str__(self):
        return f"{self.user.first_name}" + " " + "CARD-ID" +f"{self.id}"
