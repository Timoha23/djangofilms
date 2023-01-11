# Generated by Django 3.2.16 on 2023-01-11 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0005_film_name_original'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrating',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='film', to='films.film'),
        ),
    ]