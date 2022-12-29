from django.contrib import admin
from .models import FileUpload,InfoPerYear,Threshold
# Register your models here.


admin.site.register(FileUpload)
admin.site.register(InfoPerYear)
admin.site.register(Threshold)