from rest_framework import serializers
from .models import SimilarityCheck,File,Progress





class FileSerializer(serializers.ModelSerializer):
    full_url=serializers.SerializerMethodField(read_only=True)
    file_name=serializers.CharField(read_only=True,source='file.name')
    class Meta:
        model = File
        fields = ["id", "file",'author','created_at','word_count','full_url','file_name']
        
    def get_full_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url)
        
class SimilarityCheckSerialiazer(serializers.ModelSerializer):
    
    class Meta:
        model=SimilarityCheck
        fields=['id','file','year_info','author','created_at']



class ProgressSerialiazer(serializers.ModelSerializer):
    class Meta:
        model=Progress
        fields=['id','completed_file','progress','complete','threshold','task','status']