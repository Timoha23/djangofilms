# Generated by Django 3.2.16 on 2023-01-11 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_auto_20230111_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='image',
            field=models.CharField(max_length=1024),
        ),
    ]
