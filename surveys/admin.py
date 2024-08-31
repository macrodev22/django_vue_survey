from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Survey)
admin.site.register(models.SurveyAnswer)
admin.site.register(models.SurveyQuestion)
admin.site.register(models.SurveyQuestionAnswer)
admin.site.register(models.User)