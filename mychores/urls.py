from django.contrib import admin
from django.urls import path
from mychores import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scoreboard/',views.scoreboard,name='scoreboard'),
    path('taskCategories/', views.taskCategories, name = 'categories'),
    path('taskOverview/', views.taskOverview, name = 'overview'),
    path('task/<str:taskCat>,', views.taskDeets, name = 'task-detail'),
    path('done/<uuid:taskID>',views.taskDone,name='task-done'),
    path('verified/<uuid:taskID>',views.taskVerified,name='task-verified'),
    path('createNewTask',views.createNewTask,name='create-new-task'),
    path('createTaskInstance', views.newTaskInstance, name='create-task-instance'),
]
