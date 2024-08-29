from django.contrib import admin
from . import models


@admin.register(models.Menu)
class Menu(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(models.MenuItem)
class MenuItem(admin.ModelAdmin):
    list_display = ('pk', 'title', 'menu')
