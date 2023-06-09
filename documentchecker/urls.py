from django.urls import path

from .views import UploadFile, TaskView, DriveView

urlpatterns = [
    # path("file/<int:id>/", UploadFile.as_view(), name="get-view"),
    path("file/", UploadFile.as_view(), name="fileupload-view"),
    path("task/<int:id>/", TaskView.as_view(), name="similarity-detail-view"),
    path("task/", TaskView.as_view(), name="document-similarity-view"),
    path("drive/", DriveView.as_view(), name="drive-view"),
]
