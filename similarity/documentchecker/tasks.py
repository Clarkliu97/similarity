from similarity.celery import app
from .models import File,Threshold,SimilarityCheck,Progress
from thefuzz import fuzz
from docx import Document
from django.db.models import Sum
from itertools import permutations




def extracttext(file):
    doc=Document(file)
    docText = '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)
    return docText


@app.task()
def similaritycheck(*args, **kwargs):
    id = kwargs['id']
    
    similarity_obj=SimilarityCheck.objects.get(id=id)
    progress_obj=Progress()
    progress_obj.task=similarity_obj
    
    progress_obj.save()
    config = Threshold.objects.get()
    
    list_of_id = kwargs['file']
    
        
    author     =kwargs['author']
    objts=File.objects.filter(author=author,id__in=list_of_id)
    file_ids = [obj.id for obj in objts]
    years = [ year[0].year for year in objts.values_list('created_at')]
    distinct_years = list(set(years))
    data_dict = {}
    year_info_list=[]
    for year in distinct_years:
        
        
        data_dict["year"] = year
        year_querset=objts.filter(created_at__year=year)
        file_per_year=year_querset.values_list('file').count()
        data_dict['file_count'] = file_per_year
        word_count_per_year = year_querset.aggregate(words_count=Sum('word_count'))
        data_dict['word_count'] = word_count_per_year['words_count']
        year_info_list.append(data_dict)
        
        
    similarity_obj.year_info= year_info_list
    similarity_obj.save()
    pass_list=[]
    
    list_perm = [item for item in permutations(file_ids, r = 2)]
    for i,item in enumerate(list_perm):
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
            pass_list.append(item[0])
            pass_list.append(item[1])
            
        else:
            try:
                first_element=File.objects.get(id=item[0])
            except File.DoesNotExist:
                return None
            try:
                Seocnd_element=File.objects.get(id=item[1])
            except File.DoesNotExist:
                return None
            if first_element.created_at > Seocnd_element.created_at:
                pass_list.append(Seocnd_element.id)
            else:
                pass_list.append(first_obj.id)
            
        j=i+1   
        progress=round(j/len(list_perm),1) * 100
        progress_obj.progress=progress
        progress_obj.status='Inprogress'
        similarity_obj.save()
    
    pass_list= list(set(pass_list))   

    progress_obj.threshold=config.min_file
    progress_obj.save()
    if progress_obj.progress==100.0:
        similarity_obj.pass_file =len(pass_list)    
        
        if pass_list:
            for id in pass_list:
                similarity_obj.file.add(id)        
                similarity_obj.save()

            
                
                progress_obj.completed_file +=1
                progress_obj.save()
    if progress_obj.completed_file == len(pass_list):
        progress_obj.status='Complete'
        progress_obj.complete=True
        progress_obj.save()
        
    