# Generated by Django 5.0 on 2024-05-10 06:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_remove_groupe_etudiants'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupeEtudiant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.students')),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.groupe')),
            ],
        ),
        migrations.AddField(
            model_name='groupe',
            name='etudiants',
            field=models.ManyToManyField(through='main_app.GroupeEtudiant', to='main_app.students'),
        ),
    ]