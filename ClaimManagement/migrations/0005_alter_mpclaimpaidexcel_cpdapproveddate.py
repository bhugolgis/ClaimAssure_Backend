# Generated by Django 4.1.5 on 2023-03-29 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClaimManagement', '0004_alter_mpclaimpaidexcel_actualregistrationdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='cpdApprovedDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
