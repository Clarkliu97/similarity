from django.shortcuts import render
import urllib.parse
import os
from django.core.files.storage import default_storage
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from docx import Document
from .models import FileUpload,InfoPerYear
from .tasks import threshold
from .serializers import DocumentInfoSerialiazer
# Create your views here.



class UploadFile(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        file = request.data.get("file", None)
        print("file>>>>>>>>>>>>.",file)
        if file is None or file=='':
            return Response({"file": "file is required"}, status=status.HTTP_400_BAD_REQUEST)
        ext = os.path.splitext(str(file))[-1].lower()
        # if file.endswith('.docx'):
        info_list=[]
        if ext == ".docx":
            doc = Document(file)
            prop = doc.core_properties
            
            author=prop.author
            year=(prop.created).year
            print(year)
            if year is None or year=='':
                return Response({"Year": "File Without Year Not Allowed {}".format(file)}, status=status.HTTP_400_BAD_REQUEST)
            print("author<<<<<<<<<<<",author)
            if author is None or author=='':
                return Response({"Author": "{} does not have author ".format(file)}, status=status.HTTP_400_BAD_REQUEST)
            full_path = "documents/" + urllib.parse.quote(file.name.replace(" ", "-"), safe="")
            file_obj= FileUpload()
            file = default_storage.save(full_path,file)
            file_obj.author=author
            file_obj.file=file
            
            file_obj.save()
            name = str(file)
            url = default_storage.url(file)
            return Response({"full_url": request.build_absolute_uri(url), "path": name,'author':author,'id': file_obj.id})
                
        # elif ext==".doc":
        #     print("hererere")
        #     docfile.delay(file=str(file))
        #     return Response("File Converted")
        else:
            return Response("File Not Valid", status=status.HTTP_400_BAD_REQUEST)
        
class DocumentCheck(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        
        file = request.data.get("id")
        print(file)
        threshold.delay(file=file)
        return Response("report", status=status.HTTP_200_OK)
        
class DocumentInfo(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = DocumentInfoSerialiazer
    queryset = InfoPerYear.objects.all().order_by('-id')
    
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        author = self.request.query_params.get("author", None)
        print(author)
        qs=FileUpload.objects.filter(author=author).values_list('id', flat=True)
        info = InfoPerYear.objects.filter(file__id__in=list(qs))
        print(info[1].file.count())