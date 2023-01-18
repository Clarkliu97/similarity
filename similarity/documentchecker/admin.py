from django.contrib import admin
from .models import File,Task, Threshold, DEFAULT_SINGLETON_INSTANCE_ID
from django.http import HttpResponseRedirect
from django.conf.urls import url
try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode 
from django.utils.translation import ugettext as _
# Register your models here.

class SingletonModelAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super(SingletonModelAdmin, self).get_urls()

        # _meta.model_name only exists on Django>=1.6 -
        # on earlier versions, use module_name.lower()
        try:
            model_name = self.model._meta.model_name
        except AttributeError:
            model_name = self.model._meta.module_name.lower()

        self.model._meta.verbose_name_plural = self.model._meta.verbose_name
        url_name_prefix = '%(app_name)s_%(model_name)s' % {
            'app_name': self.model._meta.app_label,
            'model_name': model_name,
        }
        custom_urls = [
            url(r'^history/$',
                self.admin_site.admin_view(self.history_view),
                {'object_id': str(self.singleton_instance_id)},
                name='%s_history' % url_name_prefix),
            url(r'^$',
                self.admin_site.admin_view(self.change_view),
                {'object_id': str(self.singleton_instance_id)},
                name='%s_change' % url_name_prefix),
        ]
        # By inserting the custom URLs first, we overwrite the standard URLs.
        return custom_urls + urls

    def response_change(self, request, obj):
        msg = _('%(obj)s was changed successfully.') % {'obj': force_unicode(obj)}
        if '_continue' in request.POST:
            self.message_user(request, msg + ' ' + _('You may edit it again below.'))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)
            return HttpResponseRedirect("../../")

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if object_id == str(self.singleton_instance_id):
            self.model.objects.get_or_create(pk=self.singleton_instance_id)
        return super(SingletonModelAdmin, self).change_view(
            request,
            object_id,
            form_url=form_url,
            extra_context=extra_context,
        )


    @property
    def singleton_instance_id(self):
        return getattr(self.model, 'singleton_instance_id', DEFAULT_SINGLETON_INSTANCE_ID)


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'authors', 'complete', 'completed_file', 'created_at']
    list_filter= ['complete']

class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'word_count', 'created_at']
    list_filter= ['author']

admin.site.register(File, FileAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Threshold, SingletonModelAdmin)