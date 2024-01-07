from django.contrib import admin
from . import models

# Register your models here.
# @admin.register(models.pet)
class petadmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("Name","Breed")}

admin.site.register(models.pet,petadmin)