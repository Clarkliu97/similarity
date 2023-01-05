from .models import setup_threshold
from django.urls import path

from .views import (UploadFile,DocumentCheck,ProgressView)

urlpatterns = [
    
    path('',                                 UploadFile.as_view(),                     name='fileupload-view'),
    path('document/',                        DocumentCheck.as_view(),                  name='dacument_similerity-view'),
    path('task/<int:id>/',                            DocumentCheck.as_view(),            name='similerity-detail-view'),
    path('progress/<int:task>/',                            ProgressView.as_view(),            name='Progress-detail-view'),
    path('complete/<int:task>/',                            ProgressView.as_view(),            name='Progress-detail-view'),
    
]


setup_threshold()