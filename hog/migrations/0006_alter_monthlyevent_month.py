# Generated by Django 5.1.6 on 2025-05-16 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hog', '0005_alter_monthlyevent_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyevent',
            name='month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1),
        ),
    ]
