import os
import re
import olefile
from django.http import HttpResponse
from dateutil import parser
from rest_framework import generics, status
from rest_framework.response import Response
from docx import Document
from .models import Task,File
from .tasks import similaritycheck
from .serializers import FileSerializer,TaskSerialiazer
from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, 'index.html')


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

############################################################################################
class UploadFile(generics.ListAPIView,generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = FileSerializer
    queryset = File.objects.all().order_by('-id')
    lookup_field = 'id'
    

    def post(self, request):
        
        file = request.data.get("file", None)
        print(type(file))
        if file is None or file=='':
            return Response({"file": "file is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        extension = os.path.splitext(str(file))[-1].lower()
        if extension == ".docx":
            
            try:
                doc = Document(file)
            except Exception as e:
                return Response({"file":"File is Corrupted ".format(e)},status=status.HTTP_400_BAD_REQUEST)
            
            docText = '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)
            prop = doc.core_properties
            
            
            author=prop.author
            creation_date=prop.created
            word_count=words_count(docText)
            
        elif extension=='.doc':
            ole = olefile.OleFileIO(file)
            metadata = ole.get_metadata()
            creation_date=metadata.create_time
            author=metadata.author
            author=author.decode("utf-8") 
            text = get_doc_text(file)
            word_count=words_count(text)

        else:
            return Response({"file":"File Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
     
        try:
            datetime = parser.parse(str(creation_date))
        except Exception as e:
            return Response({"file":"date formate {} ".format(e)},status=status.HTTP_400_BAD_REQUEST)

            
            
        data_dict={"file": file, 
                    'author':author,
                    "created_at":datetime,
                    'word_count':word_count
                    }
            
        if creation_date is None or creation_date=='':
            return Response({"Year": "File Without Year Not Allowed {}".format(file)}, status=status.HTTP_400_BAD_REQUEST)
        if author is None or author=='':
            return Response({"Author": "{} does not have author ".format(file)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=data_dict,context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data_dict, status=status.HTTP_200_OK)
    
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        response = HttpResponse(instance.file, content_type='text/txt')
        response['Content-Disposition'] = 'attachment; filename={}'.format(str(instance.file.name))
        return response

class TaskView(generics.RetrieveAPIView,  generics.UpdateAPIView,generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = TaskSerialiazer
    queryset = Task.objects.all().order_by('-id')
    lookup_field = 'id'
    
    def post(self, request):
        file = request.data.get("file_id")
        if len(file) < 2:
            return Response({"file":"Add more files"},status=status.HTTP_400_BAD_REQUEST)
        if file is None or file==[]:
            return Response({"file":"Select atleast two file"},status=status.HTTP_400_BAD_REQUEST)
        author = request.data.get("author")
        if author is None or author=="":
            return Response("Please Select the Author",status=status.HTTP_400_BAD_REQUEST)
        
        
        objts=objts=File.objects.filter(author=author,id__in=file)
        if len(objts)<=1:
            return Response({"file":"Select atleast two files for {}".format(author)},status=status.HTTP_400_BAD_REQUEST)
        # create and task object
        SimilarityCheck_obj=Task()
        SimilarityCheck_obj.author=author
        SimilarityCheck_obj.save()
        # call celery
        similaritycheck.delay(file=file,author=author,id=SimilarityCheck_obj.id)
        
        return Response({"task_id":SimilarityCheck_obj.id },status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        completed_file = instance.completed_file
        threshold_file=instance.threshold_file
        if completed_file < threshold_file:
            return Response({"file":"upload more file "},status=status.HTTP_400_BAD_REQUEST)        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)