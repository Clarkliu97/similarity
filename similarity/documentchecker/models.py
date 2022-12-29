from django.db import models

# Create your models here.

report_choices = [
    ('In Progress', 'In Progress'),
    ('Converted', 'Converted'),
    ('Unsuccessful', 'Unsuccessful'),
    ('Error In File', 'Error In File'),]



class FileUpload(models.Model):
    file        =    models.FileField(upload_to='documenmt/')
    author      =    models.CharField(max_length=90,null=True,blank=True)

    
    def __str__(self) -> str:
        return self.author
    
    
class Threshold(models.Model):
    similarity_score   = models.CharField(max_length=90,null=True,blank=True)
    distinct_year      = models.CharField(max_length=90,null=True,blank=True)
    file_per_year      = models.CharField(max_length=90,null=True,blank=True)
    words_per_year     = models.CharField(max_length=90,null=True,blank=True)
    total_words        = models.CharField(max_length=90,null=True,blank=True)

class Task(models.Model):
    file        =    models.FileField(upload_to='documenmt/')
    status = models.CharField(max_length=100, choices=report_choices, null=True, blank=True)
    description = models.CharField(max_length=300)
    def __str__(self) -> str:
        return self.status
    
    
class InfoPerYear(models.Model):
    year          = models.CharField(max_length=90)
    file          = models.ManyToManyField(FileUpload)
    word_count    = models.CharField(max_length=90)