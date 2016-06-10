from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    user = models.ForeignKey(User)
    totalTimeLogged = models.DurationField()

    def get_absolute_url(self):
        return reverse('app:project', kwargs={'pk' : self})

    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    time = models.DurationField()

    def __str__(self):
        return self.name
