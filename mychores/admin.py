from django.contrib import admin
from .models import Task,Task_Instance, Profile

# Register your models here.
admin.site.register(Task)
admin.site.register(Profile)

@admin.register(Task_Instance)
class TaskInAdmin(admin.ModelAdmin):
    list_display = ('taskTbd','dueDate', 'state')