# Generated by Django 4.1.4 on 2023-01-13 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_photo_height_remove_photo_width_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='link',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='livechat',
            name='chat_enable',
            field=models.BooleanField(default=False),
        ),
    ]
