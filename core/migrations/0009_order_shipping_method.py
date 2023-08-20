# Generated by Django 4.1.3 on 2023-08-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_order_order_id_order_shelf_no_order_total_fee"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="shipping_method",
            field=models.CharField(
                choices=[
                    ("air cargo", "Air Cargo"),
                    ("sea cargo", "Sea Cargo"),
                    ("land express", "Land Express"),
                    ("land cargo", "Land Cargo"),
                ],
                default="none",
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]