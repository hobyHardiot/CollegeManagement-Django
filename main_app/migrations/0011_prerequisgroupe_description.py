# Generated by Django 5.0 on 2024-05-05 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_prerequisgroupe_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='prerequisgroupe',
            name='description',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
