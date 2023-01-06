from django.db import models
from solo.models import SingletonModel
# Create your models here.

report_choices = [
    ('Complete', 'Complete'),
    ('Failed', 'Failed'),
    ('Inprogress', 'Inprogress'),]

error_choices = [
    ("file_not_found","File not found"),
    ("no_file_with_unique_content","No file with unique content"),
    ("unknown_file_extension","Unknown file extension"),
    ("unknown_author","Unknown author"),
    ("threshold_not_found","Threshold not found")
]


class File(models.Model):
    file                  =    models.FileField(upload_to='documenmt/')
    author                =    models.CharField(max_length=90,null=True,blank=True)
    created_at            = models.DateTimeField(blank=True,null=True)
    word_count            = models.CharField(max_length=90)

    
    def __str__(self) -> str:
        return self.author
    
    
class Threshold(SingletonModel):
    min_file        =   models.IntegerField(blank=True, null=True)
    similarity_score  =   models.IntegerField(blank=True, null=True)
    def __str__(self):
        return "Threshold"

    class Meta:
        verbose_name = "Threshold"
        
    
    def delete(self, *args, **kwargs):
        pass
 

class Task(models.Model):
    author                      =    models.CharField(blank=True,max_length=100)
    files                        =    models.ManyToManyField(File, blank=True)
    year_details                   =    models.JSONField( null=True, blank=True)
    progress                    =    models.FloatField(default=0, blank=True)
    complete                    =    models.BooleanField(default=False, blank=True)
    threshold_similarity        =    models.IntegerField(default=0, blank=True)
    threshold_file              =    models.IntegerField(default=0, blank=True)
    status                      =    models.CharField(max_length=100, choices=report_choices, null=True, blank=True)
    error                       =    models.CharField(max_length=100, choices=error_choices, null=True, blank=True)
    selected_files              =    models.ManyToManyField(File, related_name='selected_files', blank=True)
    completed_file              =    models.IntegerField(default=0, blank=True)
    created_at                  =    models.DateTimeField(auto_now_add=True)
    updated_at                  =    models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.author
    
    
def setup_threshold():
    try:
            try:
                obj, created = Threshold.objects.get_or_create(
                    min_file=5, similarity_score=70)
            except Exception as e:
                print("Exception", e)
                pass
    except Exception as e:
        print("exception in permission creation", e)