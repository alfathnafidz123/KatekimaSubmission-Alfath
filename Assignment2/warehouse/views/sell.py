from rest_framework import viewsets
from ..models import SellHeader, SellDetail
from ..serializer import SellHeaderSerializer, SellDetailSerializer

class SellHeaderViewSet(viewsets.ModelViewSet):
    # API endpoint for sell headers

    queryset = SellHeader.objects.filter(is_deleted=False)
    serializer_class = SellHeaderSerializer
    lookup_field = 'code'

    def perform_destroy(self, instance):
        instance.soft_delete()

class SellDetailViewSet(viewsets.ModelViewSet):
    # API endpoint for sell details

    queryset = SellDetail.objects.filter(is_deleted=False)
    serializer_class = SellDetailSerializer

    def get_queryset(self):
        header_code = self.kwargs.get('header_code')
        return self.queryset.filter(
            header__code=header_code,
            header__is_deleted=False
        )