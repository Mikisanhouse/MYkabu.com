# Generated by Django 3.1.4 on 2021-02-23 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My株site', '0002_company_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite_code',
            name='user',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
