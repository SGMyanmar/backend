from rest_framework import serializers
from .models import *
from utils.qr import generate_qr
from utils.email_sending import send_email_with_attachment
from utils.length import length
from utils.encryption import encrypt

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


class OrderSerializer(serializers.ModelSerializer):
    recipient_info = RecipientInfoSerializer()
    sender_info = SenderInfoSerializer()
    items = ItemSerializer(many=True)
    discount_coupon = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Order
        exclude = ['qr_code',]

    def create(self, validated_data):
        recipient_info_data = validated_data.pop('recipient_info')
        sender_info_data = validated_data.pop('sender_info')
        items_data = validated_data.pop('items')

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

        prefix = 'SGMM' if order.type == 'sg to mm' else 'MMSG'
        order_id = f'{prefix}-{encrypt(length(order.id, 8))}'
        
        qr_code = generate_qr(order_id)
        order.qr_code = qr_code

        send_email_with_attachment('Your order have been submitted', f'Order id - {order_id}', [order.sender_info.email], qr_code)

        return order
