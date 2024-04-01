from django.contrib import admin
from .models import App, UserApp

admin.site.register(UserApp)


class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment')
    list_filter = ('name', 'comment')


# class UserAppAdmin(admin.ModelAdmin):
#     list_display = ('user', 'app')
#     list_filter = ('user', 'app')


admin.site.register(App, AppAdmin)
# admin.site.register(UserApp, UserAppAdmin)
