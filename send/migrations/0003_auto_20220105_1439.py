# Generated by Django 3.1.2 on 2022-01-05 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('send', '0002_auto_20220105_1301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidat',
            old_name='status',
            new_name='status_msg',
        ),
        migrations.AddField(
            model_name='candidat',
            name='status_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
