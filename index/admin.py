from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Author)
admin.site.register(models.Book)
admin.site.register(models.Rent)
admin.site.register(models.Request)
admin.site.register(models.Serie)