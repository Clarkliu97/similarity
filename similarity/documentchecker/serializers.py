from rest_framework import serializers
from .models import FileUpload,InfoPerYear





# class DocumentFileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FileUpload
#         fields = ["id", "file"]
        
        
        
# class DocumentInfoSerialiazer(serializers.ModelSerializer):
#     file = serializers.SerializerMethodField()
#     class Meta:
#         model=InfoPerYear
#         fields=['id','file','year','word_count']
#         read_only_fields = ['id', 'file']
        
#     def get_file(self, obj):
#         request = self.context.get('request')
#         if request.method == "GET":
#             file_count = obj.file.all().count()
#             return file_count
#     def validate(self, attrs):
#         info_obj=InfoPerYear.objects.get()
#         world_count=attrs.get("word_count")