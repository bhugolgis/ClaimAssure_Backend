# Generated by Django 4.1.5 on 2023-04-18 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Query', '0003_claimquery_status_preauthquery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claimquery',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='preauthquery',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
