# Generated by Django 4.1.5 on 2023-04-18 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClaimManagement', '0018_mpclaimpaidexcel_query_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='query_status',
            field=models.CharField(default='Pending', max_length=255),
        ),
    ]
