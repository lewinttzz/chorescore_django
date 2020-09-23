from django.contrib import admin
from .models import Task,Task_Instance, Profile

# Register your models here.
admin.site.register(Task)
admin.site.register(Task_Instance)
admin.site.register(Profile)

