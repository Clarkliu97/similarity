from similarity.celery import app
from .models import File,Threshold,SimilarityCheck,Progress
from thefuzz import fuzz
from docx import Document
from django.db.models import Sum
from itertools import permutations


def remove_duplicate_files(file_ids):
    # Create a new list to store the unique files
    unique_files = []
    main_list=[]
    # Iterate over the list of file IDs
    for file_id in file_ids:
        # Get the file object
        file = File.objects.get(pk=file_id)

        # Check if a file with the same creation time already exists in the unique_files list
        duplicate_found = False
        for unique_file in unique_files:
            if file.created_at == unique_file.created_at:
                duplicate_found = True
                break

        # If no duplicate was found, add the file to the unique_files list
        if not duplicate_found:
            unique_files.append(file)
            main_list.append(file.id)
            

    # Return the list of unique files
    return main_list



def extracttext(file):
    doc=Document(file)
    docText = '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)
    return docText


@app.task()
def similaritycheck(*args, **kwargs):
    id = kwargs['id']
    prog_id=kwargs['progress_id']
    similarity_obj=SimilarityCheck.objects.get(id=id)
    progress_obj=Progress.objects.get(id=prog_id)
    # progress_obj.task=similarity_obj
    
    # progress_obj.save()
    config = Threshold.objects.get()
    
    list_of_id = kwargs['file']
    
        
    author     =kwargs['author']
    objts=File.objects.filter(author=author,id__in=list_of_id)
    file_ids = [obj.id for obj in objts]
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
                pass_list.append(first_element.id)
            
        j=i+1   
        progress=round(j/len(list_perm),1) * 100
        progress_obj.progress=progress
        progress_obj.status='Inprogress'
        similarity_obj.save()
        
    unique_files_id = remove_duplicate_files(pass_list)
    unique_files_id= list(set(unique_files_id)) 
    
    progress_obj.threshold=config.min_file
    progress_obj.save()
    
    
    year_objects=File.objects.filter(author=author,id__in=unique_files_id)
    years = [ year[0].year for year in year_objects.values_list('created_at')]
    distinct_years = list(set(years))
    
    data_dict = {}
    year_info_list=[]
    for year in distinct_years:
        
        data_dict["year"] = year
        year_querset=year_objects.filter(created_at__year=year)
        file_per_year=year_querset.values_list('file').count()
        data_dict['file_count'] = file_per_year
        word_count_per_year = year_querset.aggregate(words_count=Sum('word_count'))
        data_dict['word_count'] = word_count_per_year['words_count']
        year_info_list.append(data_dict)
        
    
    similarity_obj.year_info= year_info_list
    similarity_obj.save()
    if progress_obj.progress==100.0:
        
        if unique_files_id:
            for id in unique_files_id:
                similarity_obj.file.add(id)        
                similarity_obj.save()      
                
                progress_obj.completed_file +=1
                progress_obj.save()
    
    if progress_obj.completed_file == len(unique_files_id):
        progress_obj.status='Complete'
        progress_obj.save()
        
    