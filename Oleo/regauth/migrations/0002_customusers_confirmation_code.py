# Generated by Django 4.2.7 on 2023-11-24 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusers',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
