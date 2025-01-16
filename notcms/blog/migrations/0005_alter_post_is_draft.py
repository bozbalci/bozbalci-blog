# Generated by Django 5.1.5 on 2025-01-16 23:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_alter_post_summary"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="is_draft",
            field=models.BooleanField(
                default=False,
                help_text="Draft entries do not "
                "show in index pages but can be visited directly if you know the URL.",
            ),
        ),
    ]
