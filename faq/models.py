from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse

from . import snippets


# Create your models here.
class Question(models.Model):
    category = models.ForeignKey("category", on_delete=models.SET_NULL, null=True, blank=True)
    question = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    helpful = models.IntegerField(default=0)
    not_helpful = models.IntegerField(default=0)

    def get_helpful(self):
        return QuestionHelpful.objects.filter(question=self, vote=True).count()

    def get_not_helpful(self):
        return QuestionHelpful.objects.filter(question=self, vote=False).count()

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question, allow_unicode='allow_unicode' in settings.FAQ_SETTINGS)[:150]
        self.helpful = self.get_helpful()
        self.not_helpful = self.get_not_helpful()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # if using categories
        if "no_category" not in settings.FAQ_SETTINGS:
            return reverse("faq:question_detail", args=(self.category.slug, self.slug))
        else:
            return reverse("faq:question_detail", args=(self.slug,))


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    slug = models.SlugField(max_length=10, blank=True)
    helpful = models.IntegerField(default=0)
    not_helpful = models.IntegerField(default=0)

    def get_helpful(self):
        return AnswerHelpful.objects.filter(answer=self, vote=True).count()

    def get_not_helpful(self):
        return AnswerHelpful.objects.filter(answer=self, vote=False).count()

    def __str__(self):
        return self.answer

    class Meta:
        order_with_respect_to = 'question'

    def save(self, *args, **kwargs):
        # if first time saving add a new slug
        if not self.pk or not self.slug:
            new_slug = snippets.create_random_slug(5)
            while Answer.objects.filter(slug=new_slug, answer=self.answer).exists():
                new_slug = snippets.create_random_slug()
            self.slug = new_slug
        self.helpful = self.get_helpful()
        self.not_helpful = self.get_not_helpful()
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode='allow_unicode' in settings.FAQ_SETTINGS)[:50]
        return super().save(*args, **kwargs)


class FAQComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    post_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['question', '-post_time']


class AnswerHelpful(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    vote = models.BooleanField()

    def __str__(self):
        if self.vote:
            vote_var = 'like'
        else:
            vote_var = 'dislike'

        return str(self.answer) + '- ' + vote_var

    class Meta:
        ordering = ['answer', 'vote']


class QuestionHelpful(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.BooleanField()

    def __str__(self):
        if self.vote:
            vote_var = 'like'
        else:
            vote_var = 'dislike'

        return str(self.question) + '- ' + vote_var

    class Meta:
        ordering = ['question', 'vote']
