from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from mychores.models import Task_Instance, Task, Profile
from django.contrib.auth.decorators import login_required
import operator
import datetime
from mychores.forms import CreateTaskForm, CreateTaskInstance
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.

@login_required
def index(request):
    currentUser = request.user

    cats = Task.objects.filter(isActive=True)
    for task in cats:
        task.manageInstanceCreation()

    insts = Task_Instance.objects.all()
    for inst in insts:
        inst.manageInstanceState()

    upcomingTasks = list(Task_Instance.objects.all().filter(assignedProfile__user = currentUser).filter(state= 'u').order_by('-dueDate'))
    dueTasks = list(Task_Instance.objects.all().filter(assignedProfile__user = currentUser).filter(Q(state='d')|Q(state='o')).order_by('-dueDate'))
    verificationPending = list(Task_Instance.objects.all().filter(assignedProfile__user = currentUser).filter(state= 'p').order_by('-dueDate'))
    needsVerification = list(Task_Instance.objects.all().exclude(assignedProfile__user = currentUser).filter(state= 'p').order_by('-dueDate'))

    
    context = {
        'dueTasks': dueTasks,
        'upcomingTasks' : upcomingTasks,
        'verificationPending' : verificationPending,
        'needsVerification' : needsVerification,
    }

    return render(request, 'index.html', context=context)

@login_required
def scoreboard(request):
    userProfiles = list(Profile.objects.all().order_by('-score'))
    context = {
        'userProfiles': userProfiles,
    }

    return render(request, 'scoreboard.html', context=context)

@login_required
def taskCategories(request):
    taskCategories = list(Task.objects.all())
    context = {
        'taskCategories':taskCategories,
    }

    return render(request, 'taskCategories.html', context=context)

@login_required
def taskDeets(request, taskCat):
    taskInstances = list(Task_Instance.objects.all().filter(taskTbd=taskCat).order_by('-dueDate'))
    context = {
        'taskInstances':taskInstances,
        'taskCategory' : taskCat,
    }

    return render(request, 'taskDeets.html', context=context)   

@login_required
def taskOverview(request):
    allTaskInstances = list(Task_Instance.objects.all().order_by('-dueDate'))
    context = {
        'allTaskInstances': allTaskInstances,
    }

    return render(request, 'taskOverview.html', context=context)

def taskDone(request, taskID):
    taskinstance = Task_Instance.objects.get(id = taskID)
    taskinstance.checkoffTask()

    context = {}
    return redirect('index')

def taskVerified(request, taskID):
    taskinstance = Task_Instance.objects.get(id = taskID)
    currentUserProfile = request.user.profile
    taskinstance.verifyTask(currentUserProfile)

    context = {}
    return redirect('index')

def createNewTask(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            newTask = form.save()
            newTask.manageInstanceCreation()
            return HttpResponseRedirect(reverse('categories') )
    else:
        form = CreateTaskForm()

    context = {
        'form' : form,
    }
    return render(request, 'createTaskForm.html', context = context)

def newTaskInstance(request):
    if request.method == 'POST':
        form = CreateTaskInstance(request.POST)
        formmodel = form.save(commit = False)
        if form.is_valid() and not formmodel.taskTbd.isRecurrent:
            newTask = form.save()
            newTask.assignedProfile = request.user.profile
            newTask.save()
            return HttpResponseRedirect(reverse('index') )
    else:
        form = CreateTaskInstance()

    context = {
        'form' : form,
    }
    return render(request, 'createTaskInstance.html', context = context)
