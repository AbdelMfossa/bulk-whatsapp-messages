# Generated by Django 3.1.2 on 2022-04-12 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('send', '0006_auto_20220105_1522'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidat',
            options={'verbose_name': 'Candidat', 'verbose_name_plural': 'Candidats'},
        ),
        migrations.AddField(
            model_name='candidat',
            name='telephone_mere',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='candidat',
            name='telephone_pere',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
