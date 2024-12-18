# Generated by Django 5.1.4 on 2024-12-17 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="album",
            name="slug",
            field=models.SlugField(
                default="imaginal-disk", max_length=255, unique=True
            ),
            preserve_default=False,
        ),
    ]
