from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Tag(models.Model):
    """Model for a tag that can be applied to questions."""
    name = models.CharField(max_length=50, unique=True, help_text="The name of the tag.")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Question(models.Model):
    """Model for a user-submitted question."""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Answer(models.Model):
    """Model for a user-submitted answer to a question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('question', 'author') # A user can only answer a question once

    def __str__(self):
        return f"Answer by {self.author} to '{self.question.title}'"

    @property
    def upvotes(self):
        """Returns the total number of upvotes for this answer."""
        return self.votes.filter(value=Vote.UPVOTE).count()

    @property
    def downvotes(self):
        """Returns the total number of downvotes for this answer."""
        return self.votes.filter(value=Vote.DOWNVOTE).count()


class Vote(models.Model):
    """A vote on an answer by a user."""
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only vote once per answer
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{self.user} - {self.get_value_display()} on Answer {self.answer.id}"


def answer_image_upload_path(instance, filename):
    """Generates a path for uploaded answer content images: MEDIA_ROOT/answers/<answer_id>/content/<filename>."""
    return f'answers/{instance.answer.id}/content/{filename}'


class AnswerContentBlock(models.Model):
    """A block of content (text or image) for an answer, allowing for ordered content."""
    TEXT = 'text'
    IMAGE = 'image'
    CONTENT_TYPE_CHOICES = (
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
    )

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='content_blocks')
    order = models.PositiveIntegerField(help_text="The order in which this block appears in the answer.")

    content_type = models.CharField(max_length=5, choices=CONTENT_TYPE_CHOICES)
    text = models.TextField(blank=True, null=True, help_text="Text content, if this is a text block.")
    image = models.ImageField(
        upload_to=answer_image_upload_path,
        blank=True, null=True,
        help_text="Image content, if this is an image block."
    )

    class Meta:
        ordering = ['order']
        unique_together = ('answer', 'order')  # Each block in an answer must have a unique order


class Comment(models.Model):
    """A comment on either a Question or an Answer."""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relation to allow comments on different models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.content_object}"