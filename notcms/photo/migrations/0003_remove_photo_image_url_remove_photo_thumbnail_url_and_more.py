# Generated by Django 5.1.4 on 2024-12-16 06:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("photo", "0002_alter_photo_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="photo",
            name="image_url",
        ),
        migrations.RemoveField(
            model_name="photo",
            name="thumbnail_url",
        ),
        migrations.AddField(
            model_name="photo",
            name="s3_image_path",
            field=models.CharField(default="dadadad", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="photo",
            name="title",
            field=models.CharField(
                blank=True, help_text="Optional title for the photo.", max_length=255
            ),
        ),
    ]
