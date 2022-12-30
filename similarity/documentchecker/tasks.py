from similarity.celery import app
import os
from .models import FileUpload,Task,Threshold
from thefuzz import fuzz
from docx import Document
import re
from itertools import combinations




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

def extracttext(file):
    doc=Document(file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    text='\n'.join(fullText)
    rj1=re.sub(r'^$\n', '',text, flags=re.MULTILINE)
    return rj1

@app.task()
def threshold(*args, **kwargs):
    task_id = kwargs['task_id']
    task_obj = Task.objects.get(id=task_id)
    
    file = kwargs['file']
    info_list=[]
    try:
        for id in file:
            print("list")
            obj=FileUpload.objects.get(id=id)
            file=obj.file
            count_words=word_count(file)
            obj.word_count= count_words
            print(obj)
            obj.save()
            info_list.append(obj)
    except Exception as e:
        task_obj.status = 'Unsuccessful'
    task_obj.status = 'Documents Processed Successfully'

@app.task()
def similaritycheck(*args, **kwargs):
    print("similerity")
    threshold_obj = Threshold.objects.filter(active=True).first()
    list_of_id = kwargs['file']
    list = []
    ignore_list=[]
    for item in combinations(list_of_id, r = 2):
        first_id=item[0]
        second_id=item[1]
        try:
            first_obj=FileUpload.objects.get(id=item[0])
        except FileUpload.DoesNotExist:
            return None
        try:
            Seocnd_obj=FileUpload.objects.get(id=item[1])
        except FileUpload.DoesNotExist:
            return None
        obj1_text=extracttext(first_obj.file)
        obj2_text=extracttext(Seocnd_obj.file)
        inpercentage=fuzz.token_sort_ratio(obj1_text, obj2_text)
        if inpercentage < int(threshold_obj.similarity_score):
            pass
        else:
            ignore_list.append(item)
    print('delete_list',ignore_list)
        
            
        
        
    