from django.apps import AppConfig


class MusicConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notcms.music"

    def ready(self):
        import notcms.music.signals  # noqa
