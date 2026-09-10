from django.contrib import admin
from django.contrib.auth import views as auth
from django.urls import include,path
urlpatterns=[path("admin/",admin.site.urls),path("login/",auth.LoginView.as_view(template_name="registration/login.html"),name="login"),path("logout/",auth.LogoutView.as_view(),name="logout"),path("password/change/",auth.PasswordChangeView.as_view(template_name="registration/password_change.html"),name="password_change"),path("password/change/done/",auth.PasswordChangeDoneView.as_view(),name="password_change_done"),path("",include("transactions.urls"))]
