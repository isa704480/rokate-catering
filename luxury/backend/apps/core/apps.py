from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Сайт"

    def ready(self):
        # iPhone'dan yuklangan HEIC rasmlarni qabul qilish
        try:
            import pillow_heif

            pillow_heif.register_heif_opener()
        except ImportError:  # pragma: no cover
            pass
        from . import signals  # noqa: F401
