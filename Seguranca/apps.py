from django.apps import AppConfig


def create_user_groups(sender, **kwargs):
    """
    Creates the 'reviewer' and 'developer' groups if they do not exist.
    """
    from django.contrib.auth.models import Group

    Group.objects.get_or_create(name="reviewer")
    Group.objects.get_or_create(name="developer")


class SegurancaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Seguranca"

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(create_user_groups, sender=self)

