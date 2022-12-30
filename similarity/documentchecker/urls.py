from django.urls import path

from .views import (UploadFile,DocumentCheck)

urlpatterns = [
    
    path('',                                 UploadFile.as_view(),              name='fileupload-view'),
    path('document/',                        DocumentCheck.as_view(),            name='dacument_similerity-view'),
]
