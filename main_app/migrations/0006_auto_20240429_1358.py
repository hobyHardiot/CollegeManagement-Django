# Generated by Django 3.1.1 on 2024-04-29 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20240429_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='dateBirth',
            field=models.DateField(null=True, verbose_name='%m/%d/%Y'),
        ),
    ]