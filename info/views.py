from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SiteInfo, Address
from .serializers import SiteInfoSerializer, AddressSerializer

class SiteInfoView(APIView):
    def get(self, request):
        site_info = SiteInfo.objects.first()
        serializer = SiteInfoSerializer(site_info)
        return Response(serializer.data)
    

class AddressView(APIView):
    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)