"""FFMPEGWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('new_job', views.new_job, name='new_job'),
    path('view_job/<int:id>', views.view_job, name='view_job'),
    path('job_status', views.job_status, name='job_status'),
    path('job_status/<int:id>', views.job_status_specific, name='job_status_specific'),
    path('media_files', views.media_files, name='media_files'),
    path('', views.index, name='index')
]
