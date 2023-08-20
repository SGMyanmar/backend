from rest_framework import generics
from rest_framework.response import Response
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from app_auth import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.models import *
from core.serializers import *


class OrderUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, permissions.IsStaffOrSuperUser]
    authentication_classes = [JWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        rule = Rule.objects.get(type=instance.type, shipping_method=instance.shipping_method)
        for item in instance.items.all():
            if item.name == 'foods':
                item.fee = float(item.weight) * float(rule.foods)
            elif item.name == 'clothes':
                item.fee = float(item.weight) * float(rule.clothes)
            elif item.name == 'shoes and bags':
                item.fee = float(item.weight) * float(rule.shoes_and_bags)
            elif item.name == 'cosmetics':
                item.fee = float(item.weight) * float(rule.cosmetics)
            elif item.name == 'medicines':
                item.fee = float(item.weight) * float(rule.medicines)
            elif item.name == 'supplements':
                item.fee = float(item.weight) * float(rule.supplements)
            elif item.name == 'electronics':
                item.fee = float(item.weight) * float(rule.electronics)
            elif item.name == 'valuable items':
                item.fee = float(item.weight) * float(rule.valuable_items)
            item.save()


        addon_total_fee = sum(order_addon.addon_choice.fee for order_addon in instance.order_addons.all())
        instance.total_fee = sum(item.fee for item in instance.items.all()) + addon_total_fee
        instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderInvoiceAPIView(APIView):

    permission_classes = [IsAuthenticated, permissions.IsStaffOrSuperUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs.get('pk'))
        html_file_path = 'utils/invoice.html'
        pdf_file_path = f'media/pdf_files/order-{order.order_id}.pdf'
        addons = []
        for addon in order.order_addons.all():
            addons.append((addon.addon.name, addon.addon_choice.name, addon.addon_choice.fee))
        html_to_pdf(html_file_path, pdf_file_path, order=order, addons=addons)
        send_email_with_attachment('SGMyanmar Invoice', '', [
                                   order.sender_info.email], pdf_file_path)
        return Response({'status': 'invoice email sent!'}, status=200)


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated, permissions.IsStaffOrSuperUser]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        orders = list(list(Order.objects.all()).__reversed__())
        serializer = OrderViewSerializer(orders, many=True)
        return Response(serializer.data)


class OrderInfoAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderViewSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
