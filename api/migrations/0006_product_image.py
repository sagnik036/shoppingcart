# Generated by Django 3.2.1 on 2022-10-28 17:48

import api.products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_product_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to=api.products.models.upload_path),
        ),
    ]
