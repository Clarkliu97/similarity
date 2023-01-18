from similarity.celery import app
from .models import File, Task, Threshold
from thefuzz import fuzz
from django.db.models import Sum


@app.task()
def similaritycheck(*args, **kwargs):
    id = kwargs["id"]
    similarity_obj = Task.objects.get(id=id)
    similarity_obj.status = "Inprogress"
    similarity_obj.save()
    try:
        config = Threshold.get_solo()
        # add threshold in object
        similarity_obj.threshold_file = config.min_files
        similarity_obj.threshold_similarity = config.similarity_score
        similarity_obj.save()

    except Threshold.DoesNotExist:
        similarity_obj.status = "Failed"
        similarity_obj.error = 4
        similarity_obj.save()
        return None

    list_of_id = kwargs["file"]
    authors = kwargs["authors"]

    files = File.objects.filter(author__in=authors, id__in=list_of_id, is_error=False)
    file_objs = []
    if files.exists():
        # add file
        for i in files:
            similarity_obj.files.add(i.id)
            file_objs.append(i)
    else:
        similarity_obj.status = "Failed"
        similarity_obj.error = 3
        similarity_obj.save()
        return None

    # similar files will get grouped together
    groups = []
    for i in range(0, len(file_objs)):
        match_group_index = -1
        for j in range(0, len(groups)):
            for group_file in groups[j]:
                text1, error1 = group_file.clean_text
                text2, error2 = file_objs[i].clean_text
                if error1 is False and error2 is False:
                    inpercentage = fuzz.token_sort_ratio(text2, text1)
                    if inpercentage > config.similarity_score:
                        match_group_index = j
                        break
                else:
                    similarity_obj.status = "Failed"
                    similarity_obj.error = 5
                    similarity_obj.save()
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
        similarity_obj.progress = progress
        similarity_obj.save()

    progress = 100
    similarity_obj.progress = progress
    similarity_obj.save()

    unique_files_id = []
    for group in groups:
        group.sort(key=lambda x: x.created_at, reverse=False)
        unique_files_id.append(group[0].id)

    # get unique_object
    year_objects = File.objects.filter(author__in=authors, id__in=unique_files_id)
    years = [year[0].year for year in year_objects.values_list("created_at")]
    # get distinct_years
    distinct_years = list(set(years))
    distinct_years = sorted(distinct_years)
    # year info
    year_info_list = []
    for unique_year in distinct_years:
        data_dict = {}
        data_dict["year"] = unique_year
        year_querset = year_objects.filter(created_at__year=unique_year)
        data_dict["file_count"] = year_querset.values_list("file").count()
        word_count_per_year = year_querset.aggregate(words_count=Sum("word_count"))
        data_dict["word_count"] = word_count_per_year["words_count"]
        data_dict["file_ids"] = [obj.id for obj in year_querset]
        data_dict["authors"] = [obj.author for obj in year_querset]
        year_info_list.append(data_dict)

    similarity_obj.year_details = year_info_list
    similarity_obj.save()

    if similarity_obj.progress == 100.0:

        if unique_files_id:
            for id in unique_files_id:
                similarity_obj.selected_files.add(id)
                similarity_obj.save()

                similarity_obj.completed_file += 1
                similarity_obj.save()
        else:
            similarity_obj.status = "Failed"
            similarity_obj.error = 2
            similarity_obj.save()

    if similarity_obj.completed_file == len(unique_files_id):
        similarity_obj.status = "Complete"
        similarity_obj.save()
    else:

        similarity_obj.status = "Complete"
        similarity_obj.error = 1
        similarity_obj.save()
