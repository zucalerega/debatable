"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import dynamic_lookup_view, profile_list_view, home_view, report_view, follow_view

app_name = 'users'
urlpatterns = [
    path('<str:username>/', dynamic_lookup_view, name="profile"),
    path('', home_view, name="home"),
    path('<str:username>/report/', report_view, name="report"),
    path('<str:username>/follow/', follow_view, name="follow"),

]
