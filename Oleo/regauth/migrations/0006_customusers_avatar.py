# Generated by Django 3.2.5 on 2023-12-17 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regauth', '0005_alter_customusers_last_name_confirmationcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusers',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
