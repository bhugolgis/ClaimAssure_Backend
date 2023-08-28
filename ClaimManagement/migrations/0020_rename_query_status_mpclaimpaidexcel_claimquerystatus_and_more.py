# Generated by Django 4.1.5 on 2023-04-19 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClaimManagement', '0019_alter_mpclaimpaidexcel_query_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mpclaimpaidexcel',
            old_name='query_status',
            new_name='ClaimQueryStatus',
        ),
        migrations.AddField(
            model_name='mpclaimpaidexcel',
            name='preAuthQueryStatus',
            field=models.CharField(default='Pending', max_length=255),
        ),
    ]