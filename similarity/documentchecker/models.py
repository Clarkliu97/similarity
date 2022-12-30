from django.db import models

# Create your models here.

report_choices = [
    ('Files Submitted', 'Files Submitted'),
    ('Documents Processed Successfully', 'Documents Processed Successfully'),
    ('Unsuccessful', 'Unsuccessful'),]



class FileUpload(models.Model):
    file        =    models.FileField(upload_to='documenmt/')
    author      =    models.CharField(max_length=90,null=True,blank=True)
    year          = models.DateTimeField(blank=True,null=True)
    word_count    = models.CharField(max_length=90)

    
    def __str__(self) -> str:
        return self.author
    
    
class Threshold(models.Model):
    title = models.CharField(max_length=100)
    similarity_score   = models.CharField(max_length=90,null=True,blank=True)
    distinct_year      = models.CharField(max_length=90,null=True,blank=True)
    file_per_year      = models.CharField(max_length=90,null=True,blank=True)
    words_per_year     = models.CharField(max_length=90,null=True,blank=True)
    total_words        = models.CharField(max_length=90,null=True,blank=True)
    active = models.BooleanField(default=False)


class Task(models.Model):
    file        =    models.FileField(upload_to='documenmt/')
    status = models.CharField(max_length=100, choices=report_choices, null=True, blank=True)
    description = models.CharField(max_length=300)
    def __str__(self) -> str:
        return self.status