
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ItemViewSet,
    PurchaseHeaderViewSet,
    PurchaseDetailViewSet,
    SellHeaderViewSet,
    SellDetailViewSet,
    StockReportView
)

router = DefaultRouter()
router.register(r'items', ItemViewSet)              # /api/items/
router.register(r'purchase', PurchaseHeaderViewSet) # /api/purchase/
router.register(r'sell', SellHeaderViewSet)         # /api/sell/

urlpatterns = [
    path('', include(router.urls)),
    # Purchase Endpoint
    path('purchase/<str:header_code>/details/',
         PurchaseDetailViewSet.as_view({'get': 'list', 'post': 'create'})),
    # Sell endpoint
    path('sell/<str:header_code>/details/',
         SellDetailViewSet.as_view({'get': 'list', 'post': 'create'})),
    # Report endpoint
    path('report/<str:item_code>/', StockReportView.as_view()),

]

