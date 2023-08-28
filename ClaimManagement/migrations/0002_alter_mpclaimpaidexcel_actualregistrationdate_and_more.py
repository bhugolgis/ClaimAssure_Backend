# Generated by Django 4.1.5 on 2023-03-29 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClaimManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='actualRegistrationDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='claimPaidAmount',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='claimPaidDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='claimPendingDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='claimPendingUpdatedDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='claimUpdatedDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='cpdApprovedDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='cpdRejectedDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='erroneousApprovedDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='erroneousInitiatedDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='erroneousPaidDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='preauthPendingDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='preauthPendingUpdatedDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='revokedDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpclaimpaidexcel',
            name='shaApprovedDate',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
    ]
