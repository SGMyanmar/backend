from django.urls import path
from .views import *

urlpatterns = [
    path('orders/<int:pk>/update',
         OrderUpdateAPIView.as_view(), name='order-update'),
    path('orders/<int:pk>/', OrderInfoAPIView.as_view(), name='order-info'),
    path('orders/<int:pk>/invoice', OrderInvoiceAPIView.as_view(), name='order-invoice'),
    path('orders/all/', OrderListAPIView.as_view(), name='order-list'),
]
