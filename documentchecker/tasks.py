from similarity.celery import app
from .models import File, Task, Threshold
from thefuzz import fuzz
from django.db.models import Sum


@app.task()
def similaritycheck(*args, **kwargs):
    id = kwargs["id"]
    task_obj = Task.objects.get(id=id)
    task_obj.status = "Inprogress"
    task_obj.save()
    try:
        config = Threshold.get_solo()
        # add threshold in object
        task_obj.threshold_file = config.min_files
        task_obj.threshold_similarity = config.similarity_score
        task_obj.save()

    except Threshold.DoesNotExist:
        task_obj.complete = True
        
        task_obj.status = "Failed"
        task_obj.error = 4
        task_obj.save()
        return None

    list_of_id = kwargs["file"]

    files = File.objects.filter(id__in=list_of_id, is_error=False)
    file_objs = []
    if files.exists():
        # add file
        for i in files:
            task_obj.files.add(i.id)
            file_objs.append(i)
    else:
        task_obj.complete = True
        
        task_obj.status = "Failed"
        task_obj.error = 3
        task_obj.save()
        return None

    # similar files will get grouped together
    groups = []
    similarity_detail=[]
    for i in range(0, len(file_objs)):
        match_group_index = -1
        for j in range(0, len(groups)):
            
            for group_file in groups[j]:
                
                text1, error1 = group_file.clean_text
                text2, error2 = file_objs[i].clean_text
                if error1 is False and error2 is False:
                    inpercentage = fuzz.token_sort_ratio(text2, text1)
                    if inpercentage > config.similarity_score:
                        similarity_dict={}
                        similarity_dict["similarity_score"] = inpercentage
                        similarity_dict["file"] = str(file_objs[i].file.name).split('/')[-1]
                        similarity_dict["similar_file"] = str(group_file.file.name).split('/')[-1]                                                                                                                           
                        similarity_detail.append(similarity_dict)
                        match_group_index = j
                        break
                else:
                    task_obj.complete = True
                    
                    task_obj.status = "Failed"
                    task_obj.error = 5
                    task_obj.save()
                    break
            if match_group_index != -1:
                break

        if match_group_index == -1:
            # lets create new group
            groups.append([file_objs[i]])
        else:
            # append with existing group
            groups[match_group_index].append(file_objs[i])

        progress = round(i / len(file_objs), 1) * 100
        task_obj.progress = progress
        task_obj.save()

    progress = 100
    task_obj.progress = progress
    task_obj.save()

    unique_files_id = []
    for group in groups:
        group.sort(key=lambda x: x.created_at, reverse=False)
        unique_files_id.append(group[0].id)
    task_obj.similarity_details=similarity_detail
    task_obj.save()
    # get unique_object
    year_objects = File.objects.filter(id__in=unique_files_id)
    years = [year[0].year for year in year_objects.values_list("created_at")]
    # get distinct_years
    distinct_years = list(set(years))
    distinct_years = sorted(distinct_years)
    # year info
    year_info_list = []
    years_count = 0
    for unique_year in distinct_years:
        years_count += 1
        data_dict = {}
        data_dict["year"] = unique_year
        year_querset = year_objects.filter(created_at__year=unique_year)
        data_dict["file_count"] = year_querset.values_list("file").count()
        word_count_per_year = year_querset.aggregate(words_count=Sum("word_count"))
        data_dict["word_count"] = word_count_per_year["words_count"]
        if int(word_count_per_year["words_count"]) < int(config.min_words_per_year):
            data_dict["words_status"] = "More words needed"
        else:
            data_dict["words_status"] = "Words goal passed"
        if int(data_dict["file_count"]) < int(config.min_files_per_year):
            data_dict['files_status'] = "More files needed"
        else:
            data_dict['files_status'] = "Files goal passed"
        data_dict["file_ids"] = [obj.id for obj in year_querset]
        data_dict["authors"] = [obj.author for obj in year_querset]
        year_info_list.append(data_dict)
    task_obj.year_details = year_info_list
    task_obj.save()

    if task_obj.progress == 100.0:

        if unique_files_id:
            for id in unique_files_id:
                task_obj.selected_files.add(id)
                task_obj.save()

                task_obj.completed_file += 1
                task_obj.save()
        else:
            task_obj.complete = True
            
            task_obj.status = "Failed"
            task_obj.error = 2
            task_obj.save()

    if task_obj.completed_file == len(unique_files_id):
        task_obj.complete = True
        task_obj.status = "Complete"
        task_obj.save()
    else:
        task_obj.complete = True

        task_obj.status = "Complete"
        task_obj.error = 1
        task_obj.save()
