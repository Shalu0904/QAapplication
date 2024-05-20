from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import QAModel
from .serializers import QASerializer,QAListSerializer

class PostQuestionAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data=request.data
        data["user"] = request.user
        serializer = QASerializer(data)
        if serializer.is_valid(raise_exception=True):
              return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        question_text = request.data.get('question')
        try:
            question = QAModel.objects.get(question=question_text)
            if question.user == request.user:
                serializer = QASerializer(question)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("You are not authorized to view this answer.", status=status.HTTP_403_FORBIDDEN)
        except QAModel.DoesNotExist:
            return Response("Question does not exist.", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            qa = QAModel.objects.get(pk=pk)
            if qa.user != request.user:
                return Response("You are not authorized to delete this question.", status=status.HTTP_403_FORBIDDEN)
            
            qa.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except QAModel.DoesNotExist:
            return Response("Question does not exist.", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            qa = QAModel.objects.get(pk=pk)
            if qa.user != request.user:
                return Response("You are not authorized to update this question.", status=status.HTTP_403_FORBIDDEN)
            
            data = request.data
            serializer = QASerializer(qa, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except QAModel.DoesNotExist:
            return Response("Question does not exist.", status=status.HTTP_404_NOT_FOUND)

class GetAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        question_text = request.data.get('question')
        user = request.user
        try:
            question = QAListSerializer.objects.get(user=user.pk)
            serializer = QASerializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except QAModel.DoesNotExist:
            return Response("Question does not exist.", status=status.HTTP_404_NOT_FOUND)
