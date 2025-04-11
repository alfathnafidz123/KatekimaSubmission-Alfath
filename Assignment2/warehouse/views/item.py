from rest_framework import viewsets
from ..models import Item
from ..serializer import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    # API endpoint for managing items

    queryset = Item.objects.filter(is_deleted=False)
    serializer_class = ItemSerializer
    lookup_field = 'code'

    def perform_destroy(self, instance):
        instance.soft_delete()