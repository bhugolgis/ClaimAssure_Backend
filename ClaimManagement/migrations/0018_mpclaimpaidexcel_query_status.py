# Generated by Django 4.1.5 on 2023-04-18 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClaimManagement', '0017_mpclaimpaidexcel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpclaimpaidexcel',
            name='query_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]