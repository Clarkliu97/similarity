from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Task,File
from .tasks import similaritycheck
from .serializers import FileSerializer,TaskSerialiazer
from django.shortcuts import render
import json
# Create your views here.

def index(request):
    return render(request, 'index.html')

############################################################################################
class UploadFile(generics.ListAPIView,generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = FileSerializer
    queryset = File.objects.all().order_by('-id')
    lookup_field = 'id'
    

    def post(self, request):
        file = request.data.get('file', None)
        if file is None or file=='':
            return Response({"file": "file is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data,context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
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
        files = request.data.get("file_id")
        authors = request.data.get('authors')
        if len(files) < 2:
            return Response({"file":"Add more files"},status=status.HTTP_400_BAD_REQUEST)
        if files is None or files==[]:
            return Response({"file":"Select atleast two file"},status=status.HTTP_400_BAD_REQUEST)
        if authors is None or len(authors) == 0:
            return Response({"author":"Select atleast one author"},status=status.HTTP_400_BAD_REQUEST)
        
        
        objts=File.objects.filter(author__in=authors,id__in=files)
        if len(objts)<=1:
            return Response({"file":"Select atleast two files for {}".format(authors)},status=status.HTTP_400_BAD_REQUEST)

        # create and task object
        SimilarityCheck_obj=Task()
        SimilarityCheck_obj.authors=authors
        SimilarityCheck_obj.save()

        # call celery
        similaritycheck.delay(file=files,authors=authors,id=SimilarityCheck_obj.id)
        
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
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)