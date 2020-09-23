from django.shortcuts import render
from django.views import generic
from mychores.models import Task_Instance, Task, Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required
def profile(request, userStr):

    profile = get_object_or_404(Profile,user__username = userStr)
    user = profile.user
        
    taskHistory = list(Task_Instance.objects.all().filter(assignedProfile__user__username = user).filter(state= 'f').order_by('-dueDate'))
    score = profile.score

    isMe = False
    if user == request.user:
        isMe = True
    
    context = {
        'profileOwner': user,
        'score' : score,
        'taskHistory' : taskHistory,
        'isMe' : isMe,
    }

    return render(request, 'profile.html', context=context)

    