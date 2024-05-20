from rest_framework import serializers
from .models import QAModel

class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QAModel
        fields = [ 'user', 'question', 'answer', 'date_posted']


        
class QAListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QAModel
        fields = [ 'question', 'answer']