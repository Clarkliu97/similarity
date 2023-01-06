from django.contrib import admin
from .models import File,Task, Threshold, DEFAULT_SINGLETON_INSTANCE_ID
# Register your models here.

class SingletonModelAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


    @property
    def singleton_instance_id(self):
        return getattr(self.model, 'singleton_instance_id', DEFAULT_SINGLETON_INSTANCE_ID)


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'complete', 'completed_file', 'created_at']
    list_filter= ['complete']

class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'word_count', 'created_at']
    list_filter= ['author']

admin.site.register(File, FileAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Threshold, SingletonModelAdmin)