# Generated by Django 5.1.6 on 2025-04-25 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_store_opening_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='store_images/', verbose_name='Hình ảnh'),
        ),
    ]
