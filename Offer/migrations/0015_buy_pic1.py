# Generated by Django 2.2.2 on 2019-06-09 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Offer', '0014_buy_postal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='pic1',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
    ]
