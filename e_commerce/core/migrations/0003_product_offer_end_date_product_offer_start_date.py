# Generated by Django 4.1.7 on 2023-03-08 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='offer_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
