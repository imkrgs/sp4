from atexit import register
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='app-home'),
    path('home', views.home, name='app-home'),
    path("about", views.about, name='app-about'),
    path("login", views.user_login, name='app-login'),
    path("role_red", views.role_redirect, name='app-role_login'),
    path("signup", views.signup, name='app-signup'),
    path("er_signup", views.er_signup, name='app-er_signup'),
    path("demo", views.demo, name='app-demo'),
    path('user', views.userDashboard, name='app-userDashboard'),
    path('userDashboard', views.userDashboard, name='app-userDashboard'),
    path('userProfile', views.userProfile, name='app-userProfile'),
    path('userProjects', views.userProjects, name='app-userProjects'),
    path('userUpload', views.userUpload, name='app-userUpload'),
    path('userUpdate', views.userUpdate, name='app-userUpdate'),
    path('edit_profile', views.edit_profile, name='app-edit_profile'),
    path('all/', views.all_user, name='app-userlist'),
    path('upload_project', views.upload_project, name='app-upload_project'),
    path('logout', views.logout, name='app-logout'),
    path('all_project', views.allProjects, name='app-all_projects'),
    path('request_form', views.request_form, name='app-request_project'),
    path('editResponse', views.editResponse, name='app-editResponse'),
    path('editResponse', views.editResponse, name='app-editResponse'),
    path('change_password', views.change_password, name='app-change_password'),
    path('passwordChangeResponse', views.passwordChangeResponse,
         name='app-passwordChangeResponse'),
    path('requestedProject', views.requested_Project, name='app-project_request'),
    path('requestedProjectResponse', views.requestedProjectResponse,
         name='app-requestedProjectResponse'),
    path('search_result', views.search_result, name='app-search_result'),
    path('resetpassword', views.reset_password,name='app-login_reset'),
]
urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
