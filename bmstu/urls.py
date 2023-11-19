from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('bmstu_lab.urls')),
    path('admin/', admin.site.urls)
]