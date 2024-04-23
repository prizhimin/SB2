from django.apps import AppConfig
from django.conf import settings
import os


class GeneralWeeklyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'general_weekly'

    def ready(self):
        self.PATH_TO_SAVE = os.path.join(settings.BASE_DIR, 'general_weekly', 'reports')
