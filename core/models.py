from django.db import models


STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('canceled', 'Canceled'),
)

WHO_PAY = (
    ('mm pay', 'MM Pay'),
    ('sg pay', 'SG Pay'),
)

TYPE_CHOICES = (
    ('mm to sg', 'MM to SG'),
    ('sg to mm', 'SG to MM')
)

SHIPPING_METHODS = (
    ('air cargo', 'Air Cargo'),
    ('sea cargo', 'Sea Cargo'),
    ('land express', 'Land Express'),
    ('land cargo', 'Land Cargo')
)


class RecipientInfo(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    postal_code =  models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SenderInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    postal_code =  models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(models.Model):
    recipient_info = models.OneToOneField(
        RecipientInfo, on_delete=models.CASCADE)
    sender_info = models.OneToOneField(SenderInfo, on_delete=models.CASCADE)
    discount_coupon = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True)
    who_pay = models.CharField(max_length=20, choices=WHO_PAY)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.recipient_info.name}"


class Item(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name


class Rule(models.Model):
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_METHODS)
    foods = models.DecimalField(max_digits=10, decimal_places=2)
    clothes = models.DecimalField(max_digits=10, decimal_places=2)
    shoes_and_bags = models.DecimalField(max_digits=10, decimal_places=2)
    cosmetics = models.DecimalField(max_digits=10, decimal_places=2)
    medicines = models.DecimalField(max_digits=10, decimal_places=2)
    supplements = models.DecimalField(max_digits=10, decimal_places=2)
    electronics = models.DecimalField(max_digits=10, decimal_places=2)
    valuable_items = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.type} - {self.shipping_method}'


class Addon(models.Model):
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class AddonChoice(models.Model):
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE, related_name='choices')
    name = models.CharField(max_length=200)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
