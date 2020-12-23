"""superlist URL Configuration

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
from django.urls import path

import  lists.views as view

urlpatterns = [
    path(r'', view.home_page, name='home'),
    path(r'lists/the_great_list/', view.view_list, name='view_list'),
    path(r'lists/new', view.new_list, name='new_list'),
    path('admin/', admin.site.urls),
]
