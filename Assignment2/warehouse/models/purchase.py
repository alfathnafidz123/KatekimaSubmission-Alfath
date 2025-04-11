from django.db import models
from .base import SoftDeleteModel
from .item import Item


class PurchaseHeader(SoftDeleteModel):
    code = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Purchase {self.code} - {self.date}"

    class Meta:
        verbose_name = "Purchase Header"
        verbose_name_plural = "Purchase Headers"


class PurchaseDetail(SoftDeleteModel):

    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='purchase_details')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    header = models.ForeignKey(PurchaseHeader, on_delete=models.CASCADE, related_name='details')

    def __str__(self):
        return f"{self.quantity} x {self.item.code} @ {self.unit_price}"

    def save(self, *args, **kwargs):
        """
        Override save to update item stock and balance when purchase is made.
        """
        super().save(*args, **kwargs)

        # Update the associated item's stock and balance
        self.item.stock += self.quantity
        self.item.balance += self.quantity * self.unit_price
        self.item.save()

    class Meta:
        verbose_name = "Purchase Detail"
        verbose_name_plural = "Purchase Details"