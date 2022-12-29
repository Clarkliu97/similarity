from similarity.celery import app
import os
from .models import FileUpload,InfoPerYear
from thefuzz import fuzz
from docx import Document
import re
import urllib.parse
import convertapi
convertapi.api_secret = 'dVgS2ZJdhi5HIuZB'




def word_count(file):
    doc=Document(file)
    prop = doc.core_properties
    # print(dir(prop))
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    text='\n'.join(fullText)
    rj1=re.sub(r'^$\n', '',text, flags=re.MULTILINE)
    return(len(re.findall(r'\w+',rj1)))

# @app.task()
# def check(*args, **kwargs):
#     id = kwargs['id']
#     print(id)
#     list=[]
#     obj=FileUpload.objects.get(id=id)

#     file=obj.file
#     print(type(str(file)))
#     ext = os.path.splitext(str(file))[-1].lower()
#     if ext == ".docx":
#         words=word_count(file)
#         print(words)
#         obj.count_words=words
#         obj.save()

            
    

@app.task()
def threshold(*args, **kwargs):
    file = kwargs['file']
    info_list=[]
    for id in file:
        obj=FileUpload.objects.get(id=id)
       
        file=obj.file
        doc=Document(file)
        prop = doc.core_properties
        year=(prop.created).year
        count_words=word_count(file)
        dict={
            'year':year,
            'file':id,
            'count_words':count_words
        }
        info_list.append(dict)
    years = [dict['year'] for dict in info_list]
    distinct_years = list(set(years))
    
    
    for year in distinct_years:
        info_obj=InfoPerYear()
        info_obj.year = year
        info_obj.save()
        words_count=0
        for i in info_list:
            if year==i['year']:
                file=i['file']
                word=i['count_words']
                words_count +=word 
                info_obj.file.add(file)
        info_obj.word_count = words_count 
        info_obj.save()     
        
        
        
        
    
    
