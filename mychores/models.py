from django.db import models
import uuid
import datetime
from datetime import timedelta
import math
from random import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


def findSuitableProfile():
    activeProfiles = Profile.objects.filter(isActive=True).order_by('score')
    #randID = math.floor(random() * activeProfiles.count())
    
    return activeProfiles[0]

class Task(models.Model):
    description = models.CharField(max_length=20,primary_key='true', help_text='What\'s the name of the task?')

    TASK_RECURRENCE_CATEGORY = [
        ('s', 'sporadic'),
        ('r', 'recurrent'),
        ('f', 'fixed recurrent')
    ]        

    isRecurrent = models.CharField(max_length=200,choices=TASK_RECURRENCE_CATEGORY, default='s', help_text='Should the task be repeated in regular time intervals or on demand?')
    
    recurrenceFrequency = models.DurationField(help_text='How often does the task need to be done?', blank=True,null=True)
    
    maxScore = models.IntegerField(help_text='What is the maximum achievable score for task completion?')

    isActive = models.BooleanField(default = True)

    details = models.CharField(max_length=2000, help_text='What needs to be done?', blank = True, default='No detailed description available')

    
    def __str__(self):
        return self.description
    
    def manageInstanceCreation(self):
        def nestedInstanceCreate(self,lastFinished):
            newInstance = Task_Instance(
                taskTbd=self,
                state = 'u',
                dueDate=lastFinished + self.recurrenceFrequency,
                finishedDate=None,
                assignedProfile=findSuitableProfile(),
                isMostRecent=True,
                currentProjectedScore = self.maxScore,
                )
            newInstance.save()

        today = datetime.date.today()
        if self.isActive and (self.isRecurrent != 's'): #task needs to be recurrent and active for automated instance creation
            recentInstance = Task_Instance.objects.filter(taskTbd=self).filter(isMostRecent=True) #whats the last time this task was done?
            if not recentInstance:  #never done before
                    nestedInstanceCreate(self, today - self.recurrenceFrequency)   #create instance that is due today
            else:
                recInst = recentInstance.get()
                if recInst.state == 'f': #finished
                    recInst.isMostRecent = False
                    recInst.save()
                    if self.isRecurrent == 'r': #recurrent task that can be moved around
                        nestedInstanceCreate(self, recInst.finishedDate)
                    if self.isRecurrent == 'f': #taks that need to be performed at a fixed date
                        nestedInstanceCreate(self, recInst.dueDate)
            


class Task_Instance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')

    taskTbd = models.ForeignKey('Task',on_delete=models.CASCADE,help_text='What kind of task?', null = True)

    TASK_INSTANCE_STATUS = [
        ('u', 'upcoming'),
        ('d', 'due today'),
        ('o', 'overdue'),
        ('p', 'verification pending'),
        ('e', 'expired'),
        ('f', 'finished')
    ]

    state = models.CharField(max_length=200,choices=TASK_INSTANCE_STATUS, default='d')

    dueDate = models.DateField(default=datetime.date.today())

    admin_order_field = 'dueDate'

    finishedDate = models.DateField(null=True, blank = True)

    assignedProfile = models.ForeignKey('Profile',on_delete=models.CASCADE, null = True)

    verifiedBy = models.ForeignKey('Profile', related_name='verificationBy', on_delete = models.SET_NULL, null=True, blank=True)

    notes = models.CharField(max_length=200, default= 'No notes available', blank = True)

    isMostRecent = models.BooleanField(default = False)

    currentProjectedScore = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.taskTbd.description}, Due: {self.dueDate}'

    def verifyTask(self,currentUserProfile):
        self.state = 'f'
        self.verifiedBy = currentUserProfile
        self.save()

        self.assignedProfile.score = self.assignedProfile.score + self.taskTbd.maxScore
        self.assignedProfile.save()

    def checkoffTask(self):
        self.state = 'p'
        self.finishedDate = datetime.date.today()
        self.save()

    def manageInstanceState(self):
        today = datetime.date.today()
        lenience = timedelta(days = 2)
        if self.dueDate == today and self.state == 'u':
            self.state = 'd'
        if self.dueDate < today and self.state in('u','d'):
            self.state = 'o'
        if self.dueDate + lenience < today and self.state in('u','d','o'):
            self.state = 'e'
            self.isMostRecent = False
        
        self.save()

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    isActive = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('foreignProfile', args=[str(self.user.username)])


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()