# Generated by Django 5.1.4 on 2024-12-17 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0003_tag_alter_imageupload_original_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("artist", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("openscrobbler_url", models.URLField(blank=True, null=True)),
                ("discogs_url", models.URLField(blank=True, null=True)),
                ("rating", models.IntegerField(blank=True, null=True)),
                ("review", models.TextField(blank=True, null=True)),
                (
                    "cover_image",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.imageupload",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="core.tag")),
            ],
        ),
    ]
