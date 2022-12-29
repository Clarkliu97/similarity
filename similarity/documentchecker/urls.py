from django.urls import path

from .views import (UploadFile,DocumentCheck,DocumentInfo)

urlpatterns = [
    
    path('',                                 UploadFile.as_view(),              name='fileupload-view'),
    path('document/',                        DocumentCheck.as_view(),            name='dacument_similerity-view'),
    path('info/',                            DocumentInfo.as_view(),            name='dacument_info-view')         
]
