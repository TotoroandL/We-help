from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.User)
admin.site.register(models.TaskSend)
admin.site.register(models.MasterFavorite)
admin.site.register(models.MasterLike)
admin.site.register(models.GoodType)
admin.site.register(models.MasterType)
admin.site.register(models.Good)
admin.site.register(models.GoodFavorite)
admin.site.register(models.GoodCar)
admin.site.register(models.TaskTake)
admin.site.register(models.Collection)
admin.site.register(models.Competition)
admin.site.register(models.Message)
admin.site.register(models.suggestion)
admin.site.register(models.Board)
admin.site.register(models.Topic)
admin.site.register(models.Post)
admin.site.register(models.Report)
admin.site.register(models.EmailVerifyRecord)
admin.site.register(models.CollectionCompetition)
