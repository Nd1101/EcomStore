# Generated by Django 4.1.7 on 2023-03-06 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_order_total_alter_order_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
