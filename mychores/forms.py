from django import forms
from django.forms import ModelForm
from mychores.models import Task, Task_Instance
    
class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['description','isRecurrent','recurrenceFrequency','maxScore','details']

class CreateTaskInstance(ModelForm):
    class Meta:
        model = Task_Instance
        fields = ['taskTbd','dueDate']