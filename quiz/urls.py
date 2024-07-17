# quiz/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, ChoiceViewSet, ResultViewSet, submit_quiz, register, index

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'results', ResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('submit_quiz/', submit_quiz, name='submit_quiz'),
    path('register/', register, name='register'),
    path('', index, name='index'),
]
