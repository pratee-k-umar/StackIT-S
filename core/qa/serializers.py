from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Question, Answer, Tag, Comment, Vote, AnswerContentBlock


User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the author of a question or answer."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']


class AnswerContentBlockSerializer(serializers.ModelSerializer):
    """Serializer for a single block of answer content."""
    class Meta:
        model = AnswerContentBlock
        fields = ['id', 'order', 'content_type', 'text', 'image']
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
            'text': {'required': False, 'allow_null': True},
        }


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for reading/listing answers."""
    author = AuthorSerializer(read_only=True)
    content_blocks = AnswerContentBlockSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    # The vote counts are read-only properties on the model
    upvotes = serializers.IntegerField(read_only=True)
    downvotes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            'id', 'author', 'created_at', 'updated_at',
            'content_blocks', 'comments', 'upvotes', 'downvotes'
        ]

class AnswerWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating answers with their content blocks."""
    content_blocks = AnswerContentBlockSerializer(many=True)

    class Meta:
        model = Answer
        fields = ['content_blocks']

    def create(self, validated_data):
        question = self.context['question']
        author = self.context['request'].user
        content_blocks_data = validated_data.pop('content_blocks')

        with transaction.atomic():
            answer = Answer.objects.create(question=question, author=author, **validated_data)
            for block_data in content_blocks_data:
                AnswerContentBlock.objects.create(answer=answer, **block_data)
        return answer

    def update(self, instance, validated_data):
        content_blocks_data = validated_data.pop('content_blocks')

        with transaction.atomic():
            # A simple strategy is to clear existing blocks and create new ones.
            instance.content_blocks.all().delete()
            for block_data in content_blocks_data:
                AnswerContentBlock.objects.create(answer=instance, **block_data)
            instance.save()
        return instance

class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for reading/listing questions."""
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'author', 'title', 'content', 'tags',
            'created_at', 'updated_at', 'answers', 'comments'
        ]


class QuestionWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating questions."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating a vote."""
    value = serializers.ChoiceField(choices=Vote.VOTE_CHOICES)

    class Meta:
        model = Vote
        fields = ['value']

