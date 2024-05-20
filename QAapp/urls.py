from django.urls import path
from .views import PostQuestionAnswerView,GetAnswerView
urlpatterns = [
    path('postQA/', PostQuestionAnswerView.as_view(), name='postQA'),
    path('getAns/', GetAnswerView.as_view(), name='getAns'),
    

]