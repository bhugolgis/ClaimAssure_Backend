# Generated by Django 4.1.5 on 2023-03-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClaimManagement', '0006_alter_mpclaimpaidexcel_cpdrejecteddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='shaApprovedDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
