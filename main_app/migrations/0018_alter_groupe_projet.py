# Generated by Django 5.0 on 2024-05-10 06:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_groupeetudiant_prerequisgroupe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupe',
            name='projet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.projet'),
        ),
    ]