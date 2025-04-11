from django.db import models
from django.utils import timezone

class SoftDeleteModel(models.Model):
    # base model that provides soft delete functionality with created_at, updated_at, and is_deleted fields.

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True