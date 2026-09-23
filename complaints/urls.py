from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("new/", views.create_complaint, name="create_complaint"),
    path("complaint/<int:pk>/", views.complaint_detail, name="complaint_detail"),
    path("complaint/<int:pk>/update/", views.update_complaint, name="update_complaint"),
    path("login/", auth_views.LoginView.as_view(template_name="complaints/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]
