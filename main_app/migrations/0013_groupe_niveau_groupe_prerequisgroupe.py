# Generated by Django 5.0 on 2024-05-06 03:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_groupe_etudiants'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupe',
            name='niveau',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main_app.course'),
        ),
        migrations.AddField(
            model_name='groupe',
            name='prerequisGroupe',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main_app.prerequisgroupe'),
        ),
    ]