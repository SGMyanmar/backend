from django.db import models


class SiteInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    about = models.TextField()
    terms = models.TextField()

    def __str__(self):
        return "Site Info"


class Address(models.Model):
    COUNTRY_CHOICES = (
        ('myanmar', 'Myanmar'),
        ('singapore', 'Singapore'),
    )

    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.country} Address"
