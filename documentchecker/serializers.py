from rest_framework import serializers
from .models import Task, File,Threshold
import os
from docx import Document
from dateutil import parser
import olefile
import re
from rest_framework import status
from rest_framework.response import Response



class FileSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField(read_only=True)
    file_name = serializers.CharField(read_only=True, source='file.name')

    class Meta:
        model = File
        fields = ["id", "file", 'author', 'created_at', 'word_count', 'full_url', 'file_name', 'error', 'is_error']
        extra_kwargs = {
            'word_count': {'required': False},
            'error': {'required': False}
        }

    def get_full_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url)

    def validate(self, attrs):
        file = attrs.get('file', None)

        final_attrs = {
            'file': file,
            'author': "",
            'word_count': "",
            'error': None,
            'is_error': False
        }

        # get file name without extension
        file_name = str(file).split('.')[0]
        config = Threshold.get_solo()
        if len(file_name) < 1:  # file name is empty
            final_attrs['erorr'] = 0
            final_attrs['is_error'] = True

        if file is not None:
            extension = os.path.splitext(str(file))[-1].lower()
            doc = None
            prop = None
            author = None  # creator of the document
            creation_date = None  
            last_modifier = None  
            last_modified_date = None  
            word_count = 0
            if extension == ".docx":  # docx file

                try:
                    doc = Document(file)
                except Exception as e:
                    print(e)
                    final_attrs['error'] = 1
                    final_attrs['is_error'] = True

                    # return final_attrs
                    if config.show_file_error:
                        raise serializers.ValidationError({"file":"File is Corrupted ".format(e)}, code=status.HTTP_400_BAD_REQUEST) 
                if doc is not None:
                    docText = '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)
                    prop = doc.core_properties
                    word_count = words_count(docText)

                if prop is not None:
                    author = prop.author
                    creation_date = prop.created
                    last_modifier = prop.last_modified_by
                    last_modified_date = prop.modified

            elif extension == '.doc':  # doc file
                ole = olefile.OleFileIO(file)
                metadata = ole.get_metadata()
                creation_date = metadata.create_time
                author = metadata.author
                last_modifier = metadata.last_saved_by
                last_modified_date = metadata.last_saved_time
                if author is not None and author != '':
                    author = author.decode("utf-8")
                if last_modifier is not None and last_modifier != '':
                    last_modifier = last_modifier.decode("utf-8")
                if creation_date is not None and creation_date != '':
                    creation_date = creation_date.decode("utf-8")
                if last_modified_date is not None and last_modified_date != '':
                    last_modified_date = last_modified_date.decode("utf-8")

                text = get_doc_text(file)
                word_count = words_count(text)

            else:
                final_attrs['error'] = 2
                final_attrs['is_error'] = True
                # return final_attrs
                if config.show_file_error:
                    raise serializers.ValidationError({"file": "Invalid file extension {}".format(file)}, code=status.HTTP_400_BAD_REQUEST)
                else:
                    return final_attrs
                    
            if creation_date is None or creation_date == '':
                final_attrs['error'] = 3
                final_attrs['is_error'] = True
                # return final_attrs
                if config.show_file_error:
                    raise serializers.ValidationError({"Year": "File Without Year Not Allowed {}".format(file)}, code=status.HTTP_400_BAD_REQUEST)
            try:
                creation_date = parser.parse(str(creation_date))
            except Exception as e:
                print(e)
                final_attrs['error'] = 4
                final_attrs['is_error'] = True
                # return final_attrs
                if config.show_file_error:
                    raise serializers.ValidationError({"file":"date formate {} ".format(e)}, code=status.HTTP_400_BAD_REQUEST)

            if int(word_count) == 0:
                final_attrs['error'] = 5
                final_attrs['is_error'] = True
                # return final_attrs
                if config.show_file_error:
                    raise serializers.ValidationError({'file': 'file without words not allowed {}'.format(file)}, code=status.HTTP_400_BAD_REQUEST)
            if author is None or author == '':
                final_attrs['error'] = 6
                final_attrs['is_error'] = True
                # return final_attrs
                if config.show_file_error:
                    raise serializers.ValidationError({"Author": "{} does not have author ".format(file)}, code=status.HTTP_400_BAD_REQUEST)

            final_attrs["file"] = file
            final_attrs["author"] = author
            # final_attrs["created_at"] = creation_date
            final_attrs["created_at"] = last_modified_date
            final_attrs["word_count"] = word_count

            if not author.casefold() == last_modifier.casefold():  # author and last modifier are not same
                final_attrs['error'] = 7
                final_attrs['is_error'] = True
                # return final_attrs
                if config.show_file_error:
                    raise serializers.ValidationError({"Author": "Author and Last Modifier are not same {} ".format(file)}, code=status.HTTP_400_BAD_REQUEST)

            return final_attrs


class TaskSerialiazer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'authors', 'files', 'year_details', 'progress', 'complete', 'threshold_similarity',
                  'threshold_file', 'status', 'error', 'selected_files', 'completed_file', 'created_at', 'updated_at']


def words_count(docText):
    return (len(re.findall(r'\w+', docText)))


def get_doc_text(file):
    import tempfile
    tempf, tempfn = tempfile.mkstemp(suffix='.doc')
    for chunk in file.chunks():
        os.write(tempf, chunk)
    from subprocess import Popen, PIPE
    cmd = ['antiword', tempfn]
    p = Popen(cmd, stdout=PIPE)
    stdout, _ = p.communicate()
    text = stdout.decode('ascii', 'ignore')
    return text
