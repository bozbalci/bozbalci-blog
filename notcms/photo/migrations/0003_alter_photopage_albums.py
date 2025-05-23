# Generated by Django 5.2.1 on 2025-05-24 02:17

import modelcluster.fields
from django.db import migrations

import notcms.photo.models


class Migration(migrations.Migration):
    dependencies = [
        ("photo", "0002_photoalbumsindexpage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photopage",
            name="albums",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True,
                limit_choices_to=notcms.photo.models.limit_photo_page_album_choices,
                related_name="photos",
                to="photo.photoalbumpage",
            ),
        ),
    ]
