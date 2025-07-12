from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'tags', views.TagViewSet, basename='tag')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),

    # Nested route for answers within a question
    # GET, POST -> /api/qa/questions/{question_pk}/answers/
    path('questions/<int:question_pk>/answers/', views.AnswerViewSet.as_view({'get': 'list', 'post': 'create'}), name='question-answers'),

    # Route for voting on a specific answer
    # POST -> /api/qa/answers/{answer_pk}/vote/
    path('answers/<int:answer_pk>/vote/', views.VoteView.as_view(), name='answer-vote'),
]

