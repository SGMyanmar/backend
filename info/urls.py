from django.urls import path
from .views import SiteInfoView, AddressView

urlpatterns = [
    path('site-info/', SiteInfoView.as_view(), name='site-info'),
    path('address/', AddressView.as_view(), name='address'),
]
