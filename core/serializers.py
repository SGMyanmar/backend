from rest_framework import serializers
from .models import *
from utils.qr import generate_qr
from utils.email_sending import send_email_with_attachment
from utils.length import length
from utils.encryption import encrypt
from utils.pdf import html_to_pdf


class SampleEmailSerializer(serializers.Serializer):
    data1 = serializers.CharField(required=True)
    data2 = serializers.CharField(required=True)
    data3 = serializers.CharField(required=True)


class RecipientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipientInfo
        fields = '__all__'


class SenderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenderInfo
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['order']


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddonChoice
        fields = '__all__'


class AddonSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Addon
        fields = '__all__'


class OrderAddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddon
        exclude = ['order',]


class OrderAddonViewSerializer(serializers.ModelSerializer):
    addon = AddonSerializer()
    addon_choice = ChoiceSerializer()

    class Meta:
        model = OrderAddon
        exclude = ['order',]


class OrderViewSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(allow_null=True, required=False)
    total_fee = serializers.CharField(allow_null=True, required=False)
    shelf_no = serializers.CharField(allow_null=True, required=False)
    recipient_info = RecipientInfoSerializer()
    sender_info = SenderInfoSerializer()
    items = ItemSerializer(many=True)
    order_addons = OrderAddonViewSerializer(many=True)
    discount_coupon = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

from drf_writable_nested import WritableNestedModelSerializer

class OrderSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    order_id = serializers.CharField(allow_null=True, required=False)
    total_fee = serializers.CharField(allow_null=True, required=False)
    shelf_no = serializers.CharField(allow_null=True, required=False)
    recipient_info = RecipientInfoSerializer()
    sender_info = SenderInfoSerializer()
    items = ItemSerializer(many=True)
    order_addons = OrderAddonSerializer(many=True)
    discount_coupon = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Order
        exclude = ['qr_code',]

    def create(self, validated_data):
        recipient_info_data = validated_data.pop('recipient_info')
        sender_info_data = validated_data.pop('sender_info')
        items_data = validated_data.pop('items')
        order_addons_data = validated_data.pop(
            'order_addons')  # Added this line

        recipient_info = RecipientInfo.objects.create(**recipient_info_data)
        sender_info = SenderInfo.objects.create(**sender_info_data)

        order = Order.objects.create(
            recipient_info=recipient_info,
            sender_info=sender_info,
            **validated_data
        )

        items = []
        for item_data in items_data:
            item = Item.objects.create(**item_data, order=order)
            items.append(item)

        order.items.set(items)

        addons = []
        for order_addon_data in order_addons_data:
            order_addon = OrderAddon.objects.create(
                order=order, **order_addon_data)
            addons.append(order_addon)

        order.order_addons.set(addons)  # Assign order_addons to the order

        prefix = 'SGMM' if order.type == 'sg to mm' else 'MMSG'
        order.order_id = f'{prefix}-{encrypt(length(order.id, 8))}'

        qr_code = generate_qr(order.order_id)
        order.qr_code = qr_code
        order.save()
        addons = []
        for addon in order.order_addons.all():
            addons.append((addon.addon.name, addon.addon_choice.name, addon.addon_choice.fee))
        html_file_path = 'utils/input.html'
        pdf_file_path = f'media/pdf_files/{order.order_id}.pdf'
        html_to_pdf(html_file_path, pdf_file_path, order=order,
                    order_id=order.order_id, items=list(items), addons=addons)

        send_email_with_attachment('SGMyammr Parcel Pending',
                                   f'Order id - {order.order_id}', [order.sender_info.email], pdf_file_path)

        return order
    
