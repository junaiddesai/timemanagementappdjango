from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import View
from app.forms import UserForm, ProjectForm, JobForm
from app.models import Project, Job

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'app/index.html',{ 'title': 'Home Page', 'year': '2016' })


@login_required
def appHome(request):
    """Renders the App home page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'app/appHome.html',{ 'title': 'App Home Page', 'year': '2016' })


@login_required
def projects(request):
    if not request.user.is_authenticated():
        return render(request, '/login.html')
    else:
        projects = Project.objects.filter(user=request.user)
        return render(request, 'app/projects.html', {'title': 'Projects', 'projects': projects})


@login_required
def project_detail(request, project_id):
    if not request.user.is_authenticated():
        return render(request, '/login.html')
    else:
        user = request.user
        project = get_object_or_404(Project, pk=project_id)
        jobs = Job.objects.filter(project=project)
        return render(request, 'app/project_detail.html', {'title': 'Project Details', 'project': project, 'user': user, 'jobs' : jobs})


@login_required
def create_project(request):
    if not request.user.is_authenticated():
        return render(request, '/login.html')
    else:
        form = ProjectForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            jobs = Job.objects.filter(project=project)
            return render(request, 'app/project_detail.html', {'title': 'Create New Project', 'project': project, 'user': request.user, 'jobs' : jobs})

        context = {"form": form,}
        return render(request, 'app/create_project.html', context)


@login_required
def create_job(request, project_id):
    if not request.user.is_authenticated():
        return render(request, '/login.html')
    else:
        form = JobForm(request.POST or None, request.FILES or None)
        project = get_object_or_404(Project, pk=project_id)
        if form.is_valid():
            job = form.save(commit=False)
            job.project = project
            job.save()
            project.totalTimeLogged += job.time
            project.save()
            jobs = Job.objects.filter(project=project)
            return render(request, 'app/project_detail.html', {'title': 'Create New Job', 'project': project, 'user': request.user, 'jobs' : jobs})

    context = { 'project': project,'form': form}
    return render(request, 'app/create_job.html', context)


@login_required
def delete_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.delete()
    projects = Project.objects.filter(user=request.user)
    return render(request, 'app/projects.html', {'title': 'Delete Project', 'projects': projects})


@login_required
def delete_job(request, job_id, project_id):
    job = get_object_or_404(Job, pk=job_id)
    project = Project.objects.get(pk=project_id)
    project.totalTimeLogged -= job.time
    project.save()
    job.delete()
    jobs = Job.objects.filter(project=project)
    return render(request, 'app/project_detail.html', {'title': 'Delete Job', 'project': project, 'user': request.user, 'jobs' : jobs})


class UserFormView(View):
    form_class = UserForm
    template_name = 'app/register.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'title':'Register'})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # authenticate user
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('/')

        return render(request, self.template_name, {'form': form,'title':'Register' })