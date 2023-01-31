"""similarity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

# from django.conf.urls import url
from django.urls import include, re_path, path
from documentchecker.views import index
from documentchecker.views import ConfigurationsView

urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("api/documentchecker/", include("documentchecker.urls")),
    path("api/configurations/", ConfigurationsView.as_view(), name="get-configurations"),
    
]


if settings.DEBUG is True:
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS
    )
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

urlpatterns += [re_path(r"app/^(?:.*)/?$", index, name="index1")]
urlpatterns += [re_path("app/", index, name="index1")]
