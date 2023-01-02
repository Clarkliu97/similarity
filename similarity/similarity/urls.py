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
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('documentchecker/', include('documentchecker.urls')),
]


# # + static('media/', document_root=settings.MEDIA_ROOT)
# if settings.DEBUG is True:
#     import debug_toolbar
#     urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
#     urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns = urlpatterns + [path('__debug__/', include(debug_toolbar.urls))]

# # react routes
# urlpatterns += [url(r'app/^(?:.*)/?$', index, name='index1')]
# urlpatterns += [url('app/', index, name='index1')]
# # urlpatterns += [url('', index, name='index1')]
