from django.contrib import admin
from .models import File,Task, Threshold, DEFAULT_SINGLETON_INSTANCE_ID
# Register your models here.

class SingletonModelAdmin(admin.ModelAdmin):
    object_history_template = "admin/solo/object_history.html"
    change_form_template = "admin/solo/change_form.html"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


    @property
    def singleton_instance_id(self):
        return getattr(self.model, 'singleton_instance_id', DEFAULT_SINGLETON_INSTANCE_ID)




admin.site.register(File)
admin.site.register(Task)
admin.site.register(Threshold, SingletonModelAdmin)