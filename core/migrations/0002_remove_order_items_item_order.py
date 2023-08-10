# Generated by Django 4.1.3 on 2023-07-23 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="items",
        ),
        migrations.AddField(
            model_name="item",
            name="order",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="core.order",
            ),
            preserve_default=False,
        ),
    ]