import os

from django.apps import AppConfig
from django.conf import settings

class Sixmonths2024Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sixmonths2024'

    def ready(self):
        self.PATH_TO_SAVE = os.path.join(settings.BASE_DIR, 'sixmonths2024', 'reports')
