from similarity.celery import app
import os
from .models import File,Threshold,Task
from thefuzz import fuzz
from docx import Document
from django.db.models import Sum
from itertools import permutations
# from .views import get_doc_text

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
def get_doc_text(file):
    import tempfile
    tempf, tempfn = tempfile.mkstemp(suffix='.doc')
    for chunk in file.chunks():
        os.write(tempf, chunk)
    from subprocess import Popen, PIPE
    cmd = ['antiword', tempfn]
    p = Popen(cmd, stdout=PIPE)
    stdout, _ = p.communicate()
    text =  stdout.decode('ascii', 'ignore')
    return text


def extracttext(file):
    doc=Document(file)
    docText = '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)
    return docText


@app.task()
def similaritycheck(*args, **kwargs):
    
    id = kwargs['id']
    
    similarity_obj=Task.objects.get(id=id)
    similarity_obj.status='Inprogress'
    similarity_obj.save()
    
    try:
        config = Threshold.objects.get()
        # add threshold in object
        similarity_obj.threshold_file=config.min_file
        similarity_obj.threshold_similarity=config.similarity_score
        similarity_obj.save()
   
    except Threshold.DoesNotExist:
        similarity_obj.status = "Failed"
        similarity_obj.error = "threshold_not_found"
        return None        
        
    
    list_of_id = kwargs['file']
    author=kwargs['author']
    
    objts=File.objects.filter(author=author,id__in=list_of_id)
    if objts:
        # add file 
        for i in objts:
            similarity_obj.files.add(i.id)  


        file_ids = [obj.id for obj in objts]
        pass_list=[]
        list_perm = [item for item in permutations(file_ids, r = 2)]
    else:
        similarity_obj.status = "Failed"
        similarity_obj.error = "unknown_author"
        return None

    for i,item in enumerate(list_perm):
        try:
            first_obj=File.objects.get(id=item[0])
        except File.DoesNotExist:
            similarity_obj.status = "Failed"
            similarity_obj.error = "file_not_found"
            break
            

        try:
            Seocnd_obj=File.objects.get(id=item[1])
        except File.DoesNotExist:
            similarity_obj.status = "Failed"
            similarity_obj.error = "file_not_found"
            break
        
        extension_fil1 = os.path.splitext(str(first_obj.file.name))[-1].lower()
        extension_fil2 = os.path.splitext(str(Seocnd_obj.file.name))[-1].lower()
        
        
        if extension_fil1=='.docx':
            obj1_text=extracttext(first_obj.file)
        elif extension_fil1=='.doc':
            obj1_text = get_doc_text(first_obj.file)
        else:
            similarity_obj.status = "Failed"
            similarity_obj.error = "unknown_file_extension" 
            break
                        
            
        if extension_fil2=='.docx':
            obj2_text=extracttext(Seocnd_obj.file)
        elif extension_fil2=='.doc':
            obj2_text = get_doc_text(Seocnd_obj.file)
        else:
            similarity_obj.status = "Failed"
            similarity_obj.error = "unknown_file_extension" 
            break        
                    
        inpercentage=fuzz.token_sort_ratio(obj1_text, obj2_text)
        if inpercentage < config.similarity_score:
            pass_list.append(item[0])
            pass_list.append(item[1])
            
        else:
            if first_obj.created_at > Seocnd_obj.created_at:
                pass_list.append(Seocnd_obj.id)
            else:
                pass_list.append(first_obj.id)
            
        j=i+1   
        progress=round(j/len(list_perm),1) * 100
        similarity_obj.progress=progress
        similarity_obj.save()
    
    
    # remove duplicate in pass_list 
    unique_files_id = remove_duplicate_files(pass_list)
    unique_files_id= list(set(unique_files_id)) 
    
   
    # get uniques_object
    year_objects=File.objects.filter(author=author,id__in=unique_files_id)
    years = [year[0].year for year in year_objects.values_list('created_at')]
    # get distinct_years
    distinct_years = list(set(years))
    distinct_years = sorted(distinct_years)
    # year info
    year_info_list=[]
    for unique_year in distinct_years:
        data_dict = {}
        data_dict["year"] = unique_year
        year_querset=year_objects.filter(created_at__year=unique_year)
        data_dict['file_count'] = year_querset.values_list('file').count()
        word_count_per_year = year_querset.aggregate(words_count=Sum('word_count'))
        data_dict['word_count'] = word_count_per_year['words_count']
        data_dict["file_ids"]=[obj.id for obj in year_querset]
        year_info_list.append(data_dict)
    
    
    similarity_obj.year_details= year_info_list
    similarity_obj.save()
    
    if similarity_obj.progress==100.0:
        
        if unique_files_id:
            for id in unique_files_id:
                similarity_obj.selected_files.add(id)        
                similarity_obj.save()      
                
                similarity_obj.completed_file +=1
                similarity_obj.save()
        else:
            similarity_obj.status = "Failed"
            similarity_obj.error = "no_file_with_unique_content"
            similarity_obj.save()
    
    if similarity_obj.completed_file == len(unique_files_id):
        similarity_obj.status='Complete'
        similarity_obj.save()
    else:

        similarity_obj.status='Complete'
        similarity_obj.error = 'file_not_found'
        similarity_obj.save()
