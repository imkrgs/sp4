from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, logout, authenticate
from .models import N_user, Project
from django.contrib.auth.decorators import login_required
import random,string
from django.conf import settings
from tsm_app.models import request_project
from django.core.mail import send_mail
from django.template.loader import render_to_string

user_list = N_user.objects.all()
dashb = ''


def all_user(request):
    user_list = N_user.objects.all()
    return render(request, 'app/n_user.html',
                  {'user_list': user_list})

def home(request):
    token = False
    if request.GET.get('val') == 'unauthorised':
        token = True
    projects = Project.objects.all().filter(status='Approved')
    if len(projects) > 3:
        disp_projects = random.sample(projects, 3)
    else:
        disp_projects = projects
    context = {
        'projects': disp_projects,
        'token': token,
    }
    return render(request, 'app/home.html', context)

def about(request):    
    
    return render(request, 'app/about.html', {'title': 'About'})

def user_login(request):
    global dashb
    if request.method == 'POST':
        #fetching username and pass from login form
        username = request.POST['username']
        password = request.POST['password']
        #authenticating user
        user = auth.authenticate(username=username, password=password)
        #if username and password are valid(password sent on email)
        if user:
            #creating list with username and their roles
            valid = []
            for i in user_list:
                valid.append([i.username,i.role])

            #fetching last login of user using username and setting value of first login
            first=User.objects.all().filter(username=username)
            for i in first:
                print(i.last_login)
                if i.last_login:
                    first_login= False
                else:
                    first_login=True
            #if user is not loging for first time redirecting based on roles
            if not first_login:
                # print(users)
                #print(valid)
                #print(username)
                for k in valid:
                    if k[0] == username:
                        if k[1] == 'TSM':
                            auth.login(request, user)
                            dashb = 'tsm-profile'
                            return redirect('tsm-profile')
                        elif k[1] == 'User':
                            auth.login(request, user)
                            dashb = 'app-userDashboard'
                            return redirect('app-userDashboard')
            #if user is loging for first time then redirecting to reset password 
            else:
                context={
                    'username':username
                }
                return render(request, 'app/resetpassword.html',context)
        #if credentials is not correct 
        else:
            error_message = "Invalid Credentials"
            return render(request, 'app/login.html', {'message': error_message})

    else:
        return render(request, 'app/login.html', {'title': 'Login'})


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        # validations
        value={
            'first_name':first_name,
            'last_name':last_name,
            'username':username,
            'email':email
        }
        user_names=User.objects.all().filter(username=username)
        error_message = None
        if not first_name:
            error_message = "First Name required"
        elif '@teksystems.com' not in email:
            error_message = "Kindly use TGS email"
        elif not username:
            error_message = "Username required"
        elif not email:
            error_message = "Email Required"
        elif user_names:
            error_message = "Username Already Exists"

        #genaerating random password

        letters = string.ascii_lowercase
        rand_pass = random.choices(letters,k=8) # where k is the number of required rand_letters
        password="".join(rand_pass)
        #print(password)
        

        #sending random generated password to mail
        #attaching txt template 
        msg_plain = render_to_string('app/email.txt', {'username': username ,'Password': password , 'link': 'http://127.0.0.1:8000/login'})
        
        send_mail(
            'RTC',
            msg_plain,
            'djangodemo11@gmail.com',
            ['djangodemo11@gmail.com'],
            fail_silently=False,
        )
        # saving to db
        if not error_message:
            user = User.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            print('user created')
            N_user(username=username, #password1=password1, password2=password2,
                   email=email, first_name=first_name, last_name=last_name, role='User').save()
            
            return render(request, 'app/home.html', {'message': 'Signup Sucessfull'})

        else:
            print(error_message)
            data = {
                'error':error_message,
                'values':value
            }
            return render(request, 'app/signup.html', data)

    else:
        return render(request, 'app/signup.html')


def er_signup(request):
    return render(request, 'app/er_signup.html', {'title': 'SignUp'})


def demo(request):
    return render(request, 'app/demo.html', {'title': 'demo'})


@login_required(login_url='app-login')
def userDashboard(request):
    context = {
        'title': 'user | dashboar',
        'dashboard': 'active',
        'profile': '',
        'projects': '',
        'upload_project': ''
    }
    return render(request, 'app/dashboard.html', context)


@login_required(login_url='app-login')
def userProfile(request):
    cuser = user_list.filter(username=request.user.username)
    context = {
        'title': 'user | profile ',
        'dashboard': '',
        'profile': 'active',
        'projects': '',
        'upload_project': '',
        'cuser': cuser[0],
    }
    return render(request, 'app/profile.html', context)


@login_required(login_url='app-login')
def userProjects(request):
    uproject = Project.objects.all()
    sproject = []
    name = request.user.username
    for i in uproject:
        if i.user_id == name:
            sproject.append(i)

    context = {
        'uproject': sproject,
        'title': 'user | projects ',
        'dashboard': '',
        'profile': '',
        'projects': 'active',
        'upload_project': ''
    }
    return render(request, 'app/projects.html', context)


@login_required(login_url='app-login')
def userUpload(request):
    context = {
        'title': 'user | upload project',
        'dashboard': '',
        'profile': '',
        'projects': '',
        'upload_project': 'active'
    }
    return render(request, 'app/upload_project.html', context)


@login_required(login_url='app-login')
def edit_profile(request):
    cuser = user_list.filter(username=request.user.username)
    context = {
        'title': 'user | edit profile',
        'dashboard': '',
        'profile': 'active',
        'projects': '',
        'upload_project': '',
        'cuser': cuser[0],
    }
    return render(request, 'app/edit_profile.html', context)


@login_required(login_url='app-login')
def change_password(request):
    cuser = user_list.filter(username=request.user.username)
    context = {
        'title': 'user | edit profile',
        'dashboard': '',
        'profile': 'active',
        'projects': '',
        'upload_project': '',
        'cuser': cuser[0],
    }
    return render(request, 'app/change_password.html', context)


@login_required(login_url='app-login')
def passwordChangeResponse(request):
    return userProfile(request)


@login_required(login_url='app-login')
def upload_project(request):

    if request.method == 'POST':
        tittle = request.POST.get("tittle")
        description = request.POST.get("desc")
        screenshot = request.FILES["screenshot"]
        source = request.FILES["source"]
        user_id = request.user.username
        status = 'pending'

        #uploading to s3 and db

        Project(
            title=tittle, description=description, screenshot=screenshot, source=source, user_id=user_id, status=status).save()
        
        # #uploading to s3 
        # upload_file_bucket='rtcdemo'
        # sc_upload_file_key= tittle + '/' + 'sc_'+ sc
        # # source_upload_file_key=  tittle + '/' + 'source_'+ source_name

        # s3.upload_file(sc , upload_file_bucket,sc_upload_file_key )
        # # s3.upload_fileobj(source, upload_file_bucket,source_upload_file_key )
        # print("uploaded")
        

    context = {
        'title': 'user | upload project',
        'dashboard': '',
        'profile': '',
        'projects': '',
        'upload_project': 'active',
        'message': 'uploaded',
    }
    return render(request, 'app/upload_project.html', context)


def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required(login_url='app-login')
def role_redirect(request):

    print(dashb)
    return redirect(dashb)


@login_required(login_url='app-login')
def allProjects(request):
    uproject = Project.objects.all().filter(status='Approved')

    context = {
        'uproject': uproject,
        'title': 'user | projects ',
        'dashboard': '',
        'profile': '',
        'projects': 'active',
        'upload_project': ''
    }
    return render(request, 'app/all_projects.html', context)


@login_required(login_url='app-login')
def request_form(request):
    valid = []
    for i in user_list:
        if i.role == 'TSM':
            valid.append(i.username)
    print(valid)

    context = {
        'TSMs': valid,
        'username': request.user.username
    }

    return render(request, 'app/request_form.html', context)


@login_required(login_url='app-login')
def editResponse(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        tsm = request.POST['tsm']
        N_user.objects.filter(username=request.user.username).update(
            first_name=first_name, last_name=last_name, email=email, tsm=tsm)
        User.objects.filter(username=request.user.username).update(
            first_name=first_name, last_name=last_name, email=email)
        print('updated!')
    context = {
        'title': 'user | profile ',
        'dashboard': '',
        'profile': 'active',
        'projects': '',
        'upload_project': '',
        'cuser': user_list.filter(username=request.user.username)[0],
        'pupdate': True
    }
    return render(request, 'app/profile.html', context)


@login_required(login_url='app-login')
def requested_Project(request):
    projects = request_project.objects.all().filter(username=request.user.username)
    uproject = Project.objects.all()
    context = {
        'uproject': projects,
        'title': 'user | projects ',
        'dashboard': '',
        'profile': '',
        'projects': '',
        'upload_project': '',
        'requestprojects': 'active',
        'ref': uproject,
    }
    return render(request, 'app/requestedProject.html', context)


@login_required(login_url='app-login')
def requestedProjectResponse(request):
    res = False
    if request.method == 'POST':
        name = request.user.username
        pid = request.POST['pid']
        tsm = request.POST['tsm']
        projects = request_project.objects.all().filter(
            projectId=pid, username=request.user.username)
        if len(projects) == 0:
            request_project(username=name, projectId=pid, tsm=tsm).save()
        else:
            res = True
        context = {
            'uproject': request_project.objects.all().filter(username=request.user.username),
            'title': 'user | projects ',
            'dashboard': '',
            'profile': '',
            'projects': '',
            'upload_project': '',
            'requestprojects': 'active',
            'res': res,
        }
        return render(request, 'app/requestedProject.html', context)

@login_required(login_url='app-login')
def search_result(request):
    if request.method == 'POST':
        search = request.POST['search_project']
        uproject = Project.objects.all().filter(title=search).filter(status='Approved')
        error_message=''
        if not len(uproject):
            error_message='No Project With This Title Exists'
        context = {
            'uproject': uproject,
            'title': 'user | search ',
            'error':error_message
            
        }
        return render(request, 'app/search_result.html',context)

def reset_password(request):
    global dashb
    if request.method == 'POST':
        #getting filled details
        username=request.GET.get('username')
        #cp=request.POST['cp'] #currentPassword
        np=request.POST['np'] #newPassword
        cnf=request.POST['cnf']#confirm New password

        #print(username)

        #checking  newPassword and Confirm Password are same
        if cnf and np :
            if np == cnf:
            
                #updating the password
                u = User.objects.get(username=username)
                u.set_password(np)
                u.save()

                #user login after password saved to db
                auth.login(request, u)
                dashb = 'app-userDashboard'
                return redirect('app-userDashboard')
            else:
                context={
                "error_message" : "Invalid Credentials",
                "username" : username 
                }
                return render(request, 'app/resetpassword.html', context)
        else:
            context={
            "error_message" : "Please enter Password",
            "username" : username 
            }
            return render(request, 'app/resetpassword.html', context)
    else:
        return render(request, 'app/resetpassword.html')



@login_required(login_url='app-login')
def userUpdate(request):
    
    id=request.GET.get('id')
    project=Project.objects.all().filter(id=id)
    #print(project)

    if request.method == 'POST':
        title=request.POST['titles']
        print(title)
        #only updating the description of project and status
        description = request.POST["desc"]
        
        status = 'pending'


        p = Project.objects.filter(title=title)
        p.update(description=description,status=status)
         
        print('updated!')
        return redirect('app-userDashboard')
    
    context = {
            
        'title': 'user | update project',
        'dashboard': '',
        'profile': '',
        'projects': '',
        'upload_project': 'active',
        'project' : project[0]
        }
    return render(request, 'app/update_project.html', context)
