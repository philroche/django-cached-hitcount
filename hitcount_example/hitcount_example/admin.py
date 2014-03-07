from django.contrib import admin

from .models import ExampleModel
class ExampleModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(ExampleModel, ExampleModelAdmin)


