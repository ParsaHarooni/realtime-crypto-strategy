# Generated by Django 4.2 on 2023-04-05 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(verbose_name='Time')),
                ('open_price', models.DecimalField(decimal_places=2, max_digits=1000, verbose_name='Open Price')),
                ('high_price', models.DecimalField(decimal_places=2, max_digits=1000, verbose_name='High Price')),
                ('low_price', models.DecimalField(decimal_places=2, max_digits=1000, verbose_name='Low Price')),
                ('close_price', models.DecimalField(decimal_places=2, max_digits=1000, verbose_name='Close Price')),
                ('volume', models.IntegerField(verbose_name='Volume')),
                ('date', models.DateField(verbose_name='Date')),
                ('currency', models.CharField(max_length=50, verbose_name='Currency')),
                ('time_frame', models.CharField(max_length=3, verbose_name='Date')),
            ],
        ),
    ]
