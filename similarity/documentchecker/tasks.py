from similarity.celery import app
import os
from .models import File,Threshold,SimilarityCheck
from thefuzz import fuzz
from docx import Document
import re
from django.db.models import Sum
from itertools import combinations




def extracttext(file):
    doc=Document(file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    text='\n'.join(fullText)
    rj1=re.sub(r'^$\n', '',text, flags=re.MULTILINE)
    return rj1


@app.task()
def similaritycheck(*args, **kwargs):
    
    similarity_obj=SimilarityCheck()
    
    config = Threshold.objects.get()
    
    list_of_id = kwargs['file']
    print(config)
    
        
    author     =kwargs['author']
    
    objts=File.objects.filter(author=author,id__in=list_of_id)
    file_ids = [obj.id for obj in objts]
    
    years = [ year[0].year for year in objts.values_list('created_at')]
    distinct_years = list(set(years))
    print('dist year<<<<<<<<<<<',distinct_years)
    data_dict = {}
    for year in distinct_years:
        
        data_dict[year] = {}
        year_querset=objts.filter(created_at__year=year)
        file_per_year=year_querset.values_list('file').count()
        data_dict[year]['file_count'] = file_per_year
        word_count_per_year = year_querset.aggregate(words_count=Sum('word_count'))
        data_dict[year]['word_count'] = word_count_per_year['words_count']
        
        
    similarity_obj.year_info= data_dict
    
    ignore_list=[]
    pass_list=[]
    
    for item in combinations(file_ids, r = 2):
        # print('conbinatins')
        # first_id=item[0]
        # second_id=item[1]
        try:
            first_obj=File.objects.get(id=item[0])
        except File.DoesNotExist:
            return None
        try:
            Seocnd_obj=File.objects.get(id=item[1])
        except File.DoesNotExist:
            return None
        obj1_text=extracttext(first_obj.file)
        obj2_text=extracttext(Seocnd_obj.file)
        inpercentage=fuzz.token_sort_ratio(obj1_text, obj2_text)
        if inpercentage < config.similarity_score:
            pass_list.append(item)
            progress= len(pass_list)/config.min_files * 100
            similarity_obj.progress=progress
            similarity_obj.save()
        else:
            ignore_list.append(item)
    print("data_dict",data_dict)
    # for id in ignore_list:
    #     print(id[0])
    #     print(id[1])

        
            
        
        
    