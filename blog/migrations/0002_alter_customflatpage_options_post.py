# Generated by Django 5.1.4 on 2024-12-26 00:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
        ("core", "0005_alter_imageupload_original_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customflatpage",
            options={"verbose_name": "Flatpage", "verbose_name_plural": "Flatpages"},
        ),
        migrations.CreateModel(
            name="Post",
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
                ("title", models.CharField(max_length=200)),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("slug", models.SlugField()),
                ("summary", models.TextField()),
                ("body", models.TextField()),
                (
                    "is_draft",
                    models.BooleanField(
                        default=False,
                        help_text="Draft entries do not show in index pages but can be visited directly if you know the URL.",
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True, related_name="posts", to="core.category"
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True, related_name="posts", to="core.tag"
                    ),
                ),
            ],
        ),
    ]
