from django.urls import path
from .views import *

urlpatterns = [
    path('orders/<int:pk>/update',
         OrderUpdateAPIView.as_view(), name='order-update'),
    path('orders/<int:pk>/', OrderInfoAPIView.as_view(), name='order-info'),
    path('orders/', SubmitOrderAPIView.as_view(), name='submit-order'),
    path('rules/', RulesAPIView.as_view(), name='rules'),
    path('addons/', AddonsAPIView.as_view(), name='addons'),
    path('sample-email/', SendSampleEmailView.as_view(), name='send-sample-email'),
]
