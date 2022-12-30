from django.contrib import admin
from .models import FileUpload,Threshold,Task
# Register your models here.


admin.site.register(FileUpload)
admin.site.register(Threshold)
admin.site.register(Task)