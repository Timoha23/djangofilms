# Generated by Django 3.2.16 on 2023-01-11 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_alter_film_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='image',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
