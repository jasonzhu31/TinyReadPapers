"""service URL Configuration

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
from django.urls import path, re_path
from django.views.static import serve
from service.settings import MEDIA_ROOT
import login_module.views
import filesystem.views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('sayhello', login_module.views.sayHello),
    path('login', login_module.views.login),
    path('register', login_module.views.register),

    path('test', filesystem.views.test),
    path('upload_pdf', filesystem.views.upload_pdf),
    path('checkdir', filesystem.views.checkdir),
    path('listdir', filesystem.views.listdir),
    path('open', filesystem.views.open),
    path('remove', filesystem.views.remove),
    path('last_path', filesystem.views.last_path),
    path('translate', filesystem.views.translate),

    re_path(r'media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),
]
