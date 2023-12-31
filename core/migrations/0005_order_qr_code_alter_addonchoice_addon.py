# Generated by Django 4.1.3 on 2023-08-07 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_order_who_pay_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="qr_code",
            field=models.ImageField(null=True, upload_to="qr_codes/"),
        ),
        migrations.AlterField(
            model_name="addonchoice",
            name="addon",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="choices",
                to="core.addon",
            ),
        ),
    ]
