from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import request_project
from app.models import Project, N_user
# Create your views here.

tsm_list = N_user.objects.all()


@login_required(login_url='app-login')
def profile(request):
    tsm_name = tsm_list.filter(username=request.user.username)
    print(tsm_name)
    context = {
        'tsm': tsm_name[0],
    }
    return render(request, 'profile.html', context)


@login_required(login_url='app-login')
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='app-login')
def projects(request):
    projects = Project.objects.all()
    print(projects)
    context = {
        'uproject': projects
    }

    return render(request, 'projects.html', context)


@login_required(login_url='app-login')
def pendingrequest(request):
    rproject = request_project.objects.all().filter(status='pending')

    status = request.GET.get('val')  # approve
    pid = request.GET.get('pid')  # approve
    print(status)
    print(pid)
    # id=request.POST['id'] #11

    rproject.filter(projectId=pid).update(status=status)
    print('updated')
    context = {
        'rproject': rproject
    }

    return render(request, 'pendingrequest.html', context)
