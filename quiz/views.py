from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .serializers import QuestionSerializer, ChoiceSerializer, ResultSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Choice, Result
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


@csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


def index(request):
    return render(request, 'frontend/build/index.html')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request):
    user = request.user
    # 检查是否已经存在该用户的结果
    if Result.objects.filter(user=user).exists():
        return Response({'error': 'You have already submitted the quiz.'}, status=status.HTTP_400_BAD_REQUEST)

    answers = request.data.get('answers', {})
    if not answers:
        return Response({'error': 'No answers provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Collect the groups from the choices
    groups = []
    for question_id, choice_id in answers.items():
        try:
            choice = Choice.objects.get(id=choice_id)
            groups.append(choice.group)
        except Choice.DoesNotExist:
            continue

    # Save the result
    result = Result(user=user)
    result.set_groups(list(groups))
    result.save()
    return Response({'message': 'Quiz submitted successfully'}, status=status.HTTP_201_CREATED)



class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

