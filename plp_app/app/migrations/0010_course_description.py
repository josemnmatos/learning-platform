# Generated by Django 4.1.3 on 2023-01-11 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_alter_paymentdetails_privateid"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="description",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
