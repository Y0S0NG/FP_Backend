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
        return Response({'error': '你已经提交过一次问卷了～'}, status=status.HTTP_400_BAD_REQUEST)

    answers = request.data.get('answers', {})
    if not answers:
        return Response({'error': '没有完成任何问题～'}, status=status.HTTP_400_BAD_REQUEST)

    # 获取所有问题的ID
    question_ids = set(Question.objects.values_list('id', flat=True))

    # 检查是否所有问题都提供了答案
    answered_question_ids = set(answers.keys())
    if question_ids != answered_question_ids:
        missing_question_ids = question_ids - answered_question_ids
        return Response({'error': '请确保回答完所有问题～'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Collect the groups from the choices
    groups = []
    for question_id, choice_ids in answers.items():
        if not isinstance(choice_ids, list):
            choice_ids = [choice_ids]
        for choice_id in choice_ids:
            try:
                choice = Choice.objects.get(id=choice_id)
                groups.append(choice.group)
            except Choice.DoesNotExist:
                continue

    # Save the result
    result = Result(user=user)
    result.set_groups(groups)
    result.update_tendency()  # 更新tendency
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

