from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Question, Answer, Tag, Comment, Vote
from .serializers import (
    QuestionSerializer, QuestionWriteSerializer, AnswerSerializer, AnswerWriteSerializer,
    TagSerializer, CommentSerializer, VoteSerializer,
)
from .permissions import IsOwnerOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing tags.
    """
    permission_classes = [permissions.AllowAny]


class QuestionViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing, creating, and editing questions.
    """
    queryset = Question.objects.all().prefetch_related('tags', 'answers', 'comments')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return QuestionWriteSerializer
        return QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for answers, nested under a question.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Filter answers by the question_pk from the URL and prefetch related data for efficiency
        return Answer.objects.filter(
            question_id=self.kwargs['question_pk']
        ).prefetch_related('content_blocks', 'comments', 'votes')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AnswerWriteSerializer
        return AnswerSerializer
    
    def get_serializer_context(self):
        """Pass extra context (question, request) to the serializer."""
        context = super().get_serializer_context()
        if self.action in ['create', 'update', 'partial_update']:
            context['question'] = get_object_or_404(Question, pk=self.kwargs['question_pk'])
            context['request'] = self.request
        return context


class VoteView(APIView):
    """
    An API view for upvoting or downvoting an answer.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, answer_pk):
        answer = get_object_or_404(Answer, pk=answer_pk)
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            vote_value = serializer.validated_data['value']
            vote, created = Vote.objects.update_or_create(
                user=request.user,
                answer=answer,
                defaults={'value': vote_value}
            )

            # If the user sends the same vote value again, we delete the vote (toggling off)
            if not created and vote.value == vote_value:
                vote.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(VoteSerializer(vote).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

