# Generated by Django 5.1.1 on 2024-11-24 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_bid_period_bid_comment_bidperiod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidperiod',
            name='count',
            field=models.PositiveIntegerField(default=1, verbose_name='Количесвто'),
        ),
    ]
