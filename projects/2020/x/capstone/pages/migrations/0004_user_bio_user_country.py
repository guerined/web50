# Generated by Django 4.1.4 on 2023-06-26 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_qrcode_background_qrcode_background_color_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="user",
            name="country",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
