from django.db import models
from .base import SoftDeleteModel

class Item(SoftDeleteModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"