from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
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


class AddonChoiceAPIView(generics.RetrieveAPIView):
    queryset = AddonChoice.objects.all()
    serializer_class = ChoiceSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SubmitOrderAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
