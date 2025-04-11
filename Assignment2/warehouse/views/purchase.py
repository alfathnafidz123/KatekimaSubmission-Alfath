from rest_framework import viewsets
from ..models import PurchaseHeader, PurchaseDetail
from ..serializer import PurchaseHeaderSerializer, PurchaseDetailSerializer

class PurchaseHeaderViewSet(viewsets.ModelViewSet):
    # API endpoint for purchase headers
    queryset = PurchaseHeader.objects.filter(is_deleted=False)
    serializer_class = PurchaseHeaderSerializer
    lookup_field = 'code'

    def perform_destroy(self, instance):
        instance.soft_delete()

class PurchaseDetailViewSet(viewsets.ModelViewSet):
    # API endpoint for purchase details

    queryset = PurchaseDetail.objects.filter(is_deleted=False)
    serializer_class = PurchaseDetailSerializer

    def get_queryset(self):
        # Filter details by header code
        header_code = self.kwargs.get('header_code')
        return self.queryset.filter(
            header__code=header_code,
            header__is_deleted=False
        )