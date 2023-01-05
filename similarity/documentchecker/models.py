from django.db import models
from solo.models import SingletonModel
# Create your models here.

report_choices = [
    ('Started', 'Started'),
    ('Complete', 'Complete'),
    ('Failed', 'Failed'),
    ('Inprogress', 'Inprogress'),]



class File(models.Model):
    file        =    models.FileField(upload_to='documenmt/')
    author                =    models.CharField(max_length=90,null=True,blank=True)
    created_at          = models.DateTimeField(blank=True,null=True)
    word_count    = models.CharField(max_length=90)

    
    def __str__(self) -> str:
        return self.author
    
    
class Threshold(SingletonModel):
    min_file        =   models.IntegerField(blank=True, null=True)
    similarity_score  =   models.IntegerField(blank=True, null=True)
    def __str__(self):
        return "Threshold"

    class Meta:
        verbose_name = "Threshold"
 


class SimilarityCheck(models.Model):
    author           =    models.CharField(blank=True,max_length=100)
    file             =    models.ManyToManyField(File, blank=True)
    year_info        =    models.JSONField( null=True, blank=True)
    created_at       =    models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.author

class Progress(models.Model):
    completed_file   =    models.IntegerField(default=0, blank=True)
    progress         =    models.FloatField(default=0, blank=True)
    complete         =    models.BooleanField(default=False, blank=True)
    threshold        =    models.IntegerField(default=0, blank=True)
    task             =    models.ForeignKey(SimilarityCheck, on_delete=models.CASCADE , blank=True) 
    status           =    models.CharField(max_length=100, choices=report_choices, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.status
    
    
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