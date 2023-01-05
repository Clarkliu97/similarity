import os
import re
from dateutil import parser
from rest_framework import generics, status
from rest_framework.response import Response
from docx import Document
from .models import SimilarityCheck,Progress
from .tasks import similaritycheck
from .serializers import SimilarityCheckSerialiazer,FileSerializer,ProgressSerialiazer
from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, 'index.html')


def words_count(docText):
    
    return(len(re.findall(r'\w+',docText)))


class UploadFile(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = FileSerializer
    

    def post(self, request):
        
        file = request.data.get("file", None)
        if file is None or file=='':
            return Response({"file": "file is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        extension = os.path.splitext(str(file))[-1].lower()
        if extension == ".docx":
            
            try:
                doc = Document(file)
            except Exception as e:
                return Response({"file":"File is Corrupted or ".format(e)},status=status.HTTP_400_BAD_REQUEST)
            
            docText = '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)
            prop = doc.core_properties
            
            
            author=prop.author
            year=prop.created
            word_count=words_count(docText)
            
            
            try:
                datetime = parser.parse(str(year))
            except Exception as e:
                return Response({"file":"date formate {} ".format(e)},status=status.HTTP_400_BAD_REQUEST)
            if year is None or year=='':
                return Response({"Year": "File Without Year Not Allowed {}".format(file)}, status=status.HTTP_400_BAD_REQUEST)
            if author is None or author=='':
                return Response({"Author": "{} does not have author ".format(file)}, status=status.HTTP_400_BAD_REQUEST)
            
            
            data_dict={"file": file, 
                       'author':author,
                       "created_at":datetime,
                       'word_count':word_count
                       }
            serializer = self.serializer_class(data=data_dict,context={"request": self.request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(data_dict, status=status.HTTP_200_OK)
         
        else:
            return Response("File Not Valid", status=status.HTTP_400_BAD_REQUEST)


class DocumentCheck(generics.RetrieveAPIView, generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = SimilarityCheckSerialiazer
    queryset = SimilarityCheck.objects.all().order_by('-id')
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
        
        
        objts=SimilarityCheck.objects.filter(file__author=author,file__id__in=file)
        if len(objts)<=1:
            return Response({"file":"Select atleast two files for {}".format(author)},status=status.HTTP_400_BAD_REQUEST)
        progress_obj=Progress()
        progress_obj.status='Started'
        SimilarityCheck_obj=SimilarityCheck()
        SimilarityCheck_obj.author=author
        SimilarityCheck_obj.save()
        progress_obj.task=SimilarityCheck_obj
        progress_obj.save()
        similaritycheck.delay(file=file,author=author,id=SimilarityCheck_obj.id,progress_id=progress_obj.id)
        
        return Response({"task_id":SimilarityCheck_obj.id },status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
  
  
class ProgressView(generics.RetrieveAPIView, generics.UpdateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ProgressSerialiazer
    queryset = Progress.objects.all().order_by('-id')
    lookup_field = 'task'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)