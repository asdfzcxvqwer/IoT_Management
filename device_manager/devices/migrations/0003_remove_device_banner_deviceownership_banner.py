# Generated by Django 5.0.6 on 2024-07-06 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_device_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='banner',
        ),
        migrations.AddField(
            model_name='deviceownership',
            name='banner',
            field=models.ImageField(blank=True, default='default.png', upload_to=''),
        ),
    ]
