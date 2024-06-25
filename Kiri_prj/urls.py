"""
URL configuration for Kiri_prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from Kiri_app import routing

# KSH: api urls.py를 사용하기 위해 include 추가
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('Kiri_app.urls')), #api/urls.py 사용)
    path("",include(routing.websocket_urlpatterns))
]

