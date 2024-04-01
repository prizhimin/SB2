from django.db import models
from django.contrib.auth.models import User

# Список приложений
class App(models.Model):
    name = models.CharField(max_length=100, default='')
    comment = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.comment


# Приложения, доступные конкретному пользователю
class UserApp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    app = models.ManyToManyField(App, blank=True)

    def __str__(self):
        return f"{self.user.username}'s apps"

