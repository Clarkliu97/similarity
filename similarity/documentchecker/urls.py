from django.urls import path

from .views import (UploadFile,TaskView)

urlpatterns = [
    
    path('file/',                                     UploadFile.as_view(),                      name='fileupload-view'),
    path('file/<int:id>/',                             UploadFile.as_view(),                      name='get-view'),
    path('task/',                                     TaskView.as_view(),                        name='dacument_similerity-view'),
    path('task/<int:id>/',                            TaskView.as_view(),                        name='similerity-detail-view'),
    
]

