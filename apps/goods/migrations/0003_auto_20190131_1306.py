# Generated by Django 2.0.2 on 2019-01-31 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20180304_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='is_hot',
            field=models.BooleanField(default=False, help_text='是否热销', verbose_name='是否热销'),
        ),
    ]
