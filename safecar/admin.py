from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Energy)
admin.site.register(models.Gender)
admin.site.register(models.Type)
admin.site.register(models.TypeOperation)
admin.site.register(models.Vehicle)
admin.site.register(models.Agency)
admin.site.register(models.Department)
admin.site.register(models.City)
admin.site.register(models.District)
admin.site.register(models.Notification)
admin.site.register(models.Warning)
admin.site.register(models.Reader)
admin.site.register(models.Record)
admin.site.register(models.Operation)
admin.site.register(models.UserGroup)
admin.site.register(models.Owner)
admin.site.register(models.Verdict)
admin.site.register(models.Status)
admin.site.register(models.Tag)
