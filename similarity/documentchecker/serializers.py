from rest_framework import serializers
from .models import Task,File
from rest_framework import status




class FileSerializer(serializers.ModelSerializer):
    full_url=serializers.SerializerMethodField(read_only=True)
    file_name=serializers.CharField(read_only=True,source='file.name')
    class Meta:
        model = File
        fields = ["id", "file",'author','created_at','word_count','full_url','file_name']
        
    def get_full_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url)
        
class TaskSerialiazer(serializers.ModelSerializer):
    
    class Meta:
        model=Task
        fields=['id','author','files','year_details','progress','complete','threshold_similarity',
                'threshold_file','status','error','selected_files','completed_file','created_at','updated_at']