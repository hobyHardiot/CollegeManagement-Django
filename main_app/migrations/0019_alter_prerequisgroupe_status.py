# Generated by Django 5.0 on 2024-05-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0018_alter_groupe_projet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prerequisgroupe',
            name='status',
            field=models.IntegerField(),
        ),
    ]
