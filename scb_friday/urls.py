"""scb_friday URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.users.urls')),

    path('docs/', include_docs_urls(title='BlogAPI')),
    path('schema', get_schema_view(
        title="ScbFridayAPI",
        description="API for the ScbFridayAPI",
        version="1.0.0"
    ), name='openapi-schema'),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

admin.site.site_header ='Scb Friday'
admin.site.index_title ='Scb Friday'
admin.site.site_title ='Scb Friday Admin'
