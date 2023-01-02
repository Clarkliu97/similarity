from django.db import models
from solo.models import SingletonModel
# Create your models here.

report_choices = [
    ('Files Submitted', 'Files Submitted'),
    ('Documents Processed Successfully', 'Documents Processed Successfully'),
    ('Unsuccessful', 'Unsuccessful'),]



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
    file        =    models.ManyToManyField(File)
    status      =    models.CharField(max_length=100, choices=report_choices, null=True, blank=True)
    year_info   =    models.JSONField()
    progress    =    models.FloatField()
    created_at  =    models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.status