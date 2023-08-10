from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from app_auth import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

from utils import email_sending as mail


class SendSampleEmailView(APIView):
    serializer_class = SampleEmailSerializer

    def post(self, request):
        context = self.serializer_class(data=request.data)
        if context.is_valid():
            context = context.validated_data
        mail.send_sample_email(context)
        return Response({'status: sent'}, status=status.HTTP_200_OK)


class RulesAPIView(APIView):
    def get(self, request):
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        return Response(serializer.data)


class AddonsAPIView(APIView):
    def get(self, request):
        addons = Addon.objects.all()
        serializer = AddonSerializer(addons, many=True)
        return Response(serializer.data)


class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, permissions.IsStaffOrSuperUser]
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderInfoAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmitOrderAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
