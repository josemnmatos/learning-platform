<<<<<<< HEAD
# Generated by Django 4.1.3 on 2023-01-07 17:52
=======
# Generated by Django 4.1.4 on 2023-01-07 18:55
>>>>>>> cbcffd6cfc897db01fe4fad5cd2fc06ccf4974ac

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_alter_admin_userid_alter_participant_userid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursesenrolled",
            name="paymentMethod",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="app.paymentdetails",
            ),
        ),
    ]
