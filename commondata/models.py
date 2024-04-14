from django.db import models


class Department(models.Model):
    """
    Список филиалов
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name