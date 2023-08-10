# Generated by Django 4.1.3 on 2023-07-23 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("weight", models.FloatField()),
                ("quantity", models.PositiveIntegerField()),
                ("fee", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="RecipientInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=20)),
                ("address", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="SenderInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("address", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "discount_coupon",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("on_the_way", "On the Way"),
                            ("confirmed", "Confirmed"),
                            ("sending", "Sending"),
                            ("sent", "Sent"),
                            ("canceled", "Canceled"),
                        ],
                        max_length=20,
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("items", models.ManyToManyField(to="core.item")),
                (
                    "recipient_info",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.recipientinfo",
                    ),
                ),
                (
                    "sender_info",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.senderinfo",
                    ),
                ),
            ],
        ),
    ]
