from django.contrib import admin
from .models import *

class ItemInline(admin.TabularInline):
    model = Item


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'sender', 'items_info', 'discount_coupon', 'status', 'date')
    inlines = [ItemInline]

    def recipient(self, obj):
        return f"{obj.recipient_info.name} - {obj.recipient_info.phone} - {obj.recipient_info.address}"

    def sender(self, obj):
        return f"{obj.sender_info.name} - {obj.sender_info.phone} - {obj.sender_info.address}" 

    def items_info(self, obj):
        items_info_list = [
            f"{item.name} - Weight: {item.weight} - Fee: {item.fee}"
            for item in obj.items.all()
        ]
        return "\n".join(items_info_list)

    recipient.short_description = 'Recipient'
    sender.short_description = 'Sender'
    items_info.short_description = 'Items Information'

admin.site.register(Order, OrderAdmin)
admin.site.register(Rule)
admin.site.register(Addon)
admin.site.register(AddonChoice)
