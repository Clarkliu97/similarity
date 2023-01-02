from similarity.celery import app
import os
from .models import FileUpload,Task,Threshold
from thefuzz import fuzz
from docx import Document
import re
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
    
    print("similerity")
    threshold_obj = Threshold.objects.filter(active=True).first()
    list_of_id = kwargs['file']
    print("list_of_id",list_of_id)
   
    author     =kwargs['author']
    print("author",author)
    objts=FileUpload.objects.filter(author=author,id__in=list_of_id)
    file_ids = [obj.id for obj in objts]
    print("author>>>>>>>>>>>",file_ids)
    ignore_list=[]
    for item in combinations(file_ids, r = 2):
        # print('conbinatins')
        # first_id=item[0]
        # second_id=item[1]
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
        
    for id in ignore_list:
        print(id[0])
        print(id[1])

        
            
        
        
    