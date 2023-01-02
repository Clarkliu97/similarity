from django.contrib import admin
from .models import File,Threshold,SimilarityCheck
# Register your models here.


admin.site.register(File)
admin.site.register(Threshold)
admin.site.register(SimilarityCheck)