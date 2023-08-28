# Generated by Django 4.1.5 on 2023-04-04 11:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Query', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimquery',
            name='date_modified',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preauthquery',
            name='date_modified',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
