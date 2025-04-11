from django.db import models
from .base import SoftDeleteModel
from .item import Item
from .purchase import PurchaseDetail


class SellHeader(SoftDeleteModel):
    code = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Sell {self.code} - {self.date}"

    class Meta:
        verbose_name = "Sell Header"
        verbose_name_plural = "Sell Headers"


class SellDetail(SoftDeleteModel):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='sell_details')
    quantity = models.IntegerField()
    header = models.ForeignKey(SellHeader, on_delete=models.CASCADE, related_name='details')

    def __str__(self):
        return f"{self.quantity} x {self.item.code}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        remaining_quantity = self.quantity
        item = self.item

        # Get all purchase details that still have stock, ordered by date
        purchases = PurchaseDetail.objects.filter(
            item=item,
            quantity__gt=0
        ).order_by('header__date', 'id')

        # Process each purchase to deduct stock
        for purchase in purchases:
            if remaining_quantity <= 0:
                break

            # Calculate how much to deduct from this purchase
            deduct = min(purchase.quantity, remaining_quantity)
            purchase.quantity -= deduct
            purchase.save()

            # Update item stock and balance
            item.stock -= deduct
            item.balance -= deduct * purchase.unit_price
            remaining_quantity -= deduct

        item.save()

    class Meta:
        verbose_name = "Sell Detail"
        verbose_name_plural = "Sell Details"