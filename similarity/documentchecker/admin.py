from django.contrib import admin
from .models import File,Threshold,SimilarityCheck,Progress
# Register your models here.


admin.site.register(File)
admin.site.register(Threshold)
admin.site.register(SimilarityCheck)
admin.site.register(Progress)