# Generated by Django 4.1.5 on 2023-05-24 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PreAuth', '0006_merge_20230516_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preauthdocument',
            name='date_modified',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
