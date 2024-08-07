from django.apps import AppConfig
from django.conf import settings
import os


class InvestigationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investigations'

    def ready(self):
        self.PATH_TO_SAVE = os.path.join(settings.BASE_DIR, 'investigations', 'reports')
