from rest_framework import serializers
from .models import Task,File
import os
from docx import Document
from dateutil import parser
import olefile
import re
import json


class FileSerializer(serializers.ModelSerializer):
    full_url=serializers.SerializerMethodField(read_only=True)
    file_name=serializers.CharField(read_only=True,source='file.name')
    class Meta:
        model = File
        fields = ["id", "file",'author','created_at','word_count','full_url','file_name', 'error','is_error']
        extra_kwargs = {
            'word_count': {'required': False},
            'error': {'required': False}
        }

    def get_full_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url)


    def validate(self, attrs):
        file = attrs.get('file', None)

        final_attrs = {
            'file': file,
            'author': "",
            'word_count': "",
            'error': {},
            'is_error': False
        }        

        # get file name without extension
        file_name =str(file).split('.')[0]

        if len(file_name) < 1:
            final_attrs['erorr']['name'] = 'File name not valid'
            final_attrs['is_error'] = True       

        if file is not None:
            extension = os.path.splitext(str(file))[-1].lower()
            doc = None
            prop = None
            author = None
            if extension == ".docx":

                try:
                    doc = Document(file)
                except Exception as e:
                    final_attrs['error']['file'] = "File is corrupted" 
                    final_attrs['is_error'] = True       

                    return final_attrs
                    # return Response({"file":"File is Corrupted ".format(e)},status=status.HTTP_400_BAD_REQUEST)
                if doc is not None:
                    docText = '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)
                    prop = doc.core_properties

                if prop is not None:
                    author=prop.author
                    creation_date=prop.created
                word_count=words_count(docText)

            elif extension=='.doc':
                ole = olefile.OleFileIO(file)
                metadata = ole.get_metadata()
                creation_date=metadata.create_time
                author=metadata.author
                if author != None and author == '':
                    author=author.decode("utf-8") 
                    
                text = get_doc_text(file)
                word_count=words_count(text)

            else:
                final_attrs['error']['extension'] = "Invalid file extension"
                final_attrs['is_error'] = True 
                return final_attrs


            if creation_date is None or creation_date=='':
                final_attrs['error']['creation_date'] = "Creation date not found"
                final_attrs['is_error'] = True 
                return final_attrs                    
                # return Response({"Year": "File Without Year Not Allowed {}".format(file)}, status=status.HTTP_400_BAD_REQUEST)
            try:
                datetime = parser.parse(str(creation_date))
            except Exception as e:
                final_attrs['error']['date_format'] = "Invalid created date format"
                final_attrs['is_error'] = True 
                return final_attrs                
                # return Response({"file":"date formate {} ".format(e)},status=status.HTTP_400_BAD_REQUEST)

            if int(word_count) == 0:
                final_attrs['error']['word_count'] = "No words in file"
                final_attrs['is_error'] = True 
                return final_attrs                    
                # return Response({'file': 'file without words not allowed {}'.format(file)}, status=status.HTTP_400_BAD_REQUEST)
            if author is None or author=='':
                final_attrs['error']['author'] = "No author found"
                final_attrs['is_error'] = True 
                return final_attrs                    
                # return Response({"Author": "{} does not have author ".format(file)}, status=status.HTTP_400_BAD_REQUEST)

            final_attrs["file"]= file
            final_attrs["author"]=author
            final_attrs["created_at"]=datetime
            final_attrs["word_count"]=word_count
        
            return final_attrs


class TaskSerialiazer(serializers.ModelSerializer):
    
    class Meta:
        model=Task
        fields=['id','authors','files','year_details','progress','complete','threshold_similarity',
                'threshold_file','status','error','selected_files','completed_file','created_at','updated_at']


def words_count(docText):
    return(len(re.findall(r'\w+',docText)))

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