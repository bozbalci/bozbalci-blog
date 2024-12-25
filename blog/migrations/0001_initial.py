# Generated by Django 5.1.4 on 2024-12-25 08:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("flatpages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomFlatPage",
            fields=[
                (
                    "flatpage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flatpages.flatpage",
                    ),
                ),
                (
                    "is_draft",
                    models.BooleanField(
                        default=True, help_text="Mark this page as draft."
                    ),
                ),
                ("published_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("modified_at", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                "verbose_name": "NC-Flatpage",
                "verbose_name_plural": "NC-Flatpages",
            },
            bases=("flatpages.flatpage",),
        ),
    ]
