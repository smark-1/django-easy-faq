from django.contrib import admin
from .models import *
from django.conf import settings

# Register your models here.

class AnswerHelpfulAdmin(admin.ModelAdmin):
    list_display = ("vote", "answer", "user")
    list_filter = ('vote',)
    search_fields = ['answer', "user"]


class QuestionHelpfulAdmin(admin.ModelAdmin):
    list_display = ("vote", "question", "user")
    list_filter = ('vote',)
    search_fields = ['question', "user"]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("answer", "question", "helpful", "not_helpful")
    list_filter = ('helpful', "not_helpful")
    search_fields = ['answer', "question"]
    readonly_fields = ('helpful', "not_helpful", 'slug')


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', "_description"]
    readonly_fields = ("slug",)

    def get_list_display(self, request):
        if "no_category_description" not in settings.FAQ_SETTINGS:
            return ["name", "slug", "description"]
        return ['name', 'slug']

    def get_exclude(self, request, obj=None):
        if "no_category_description" in settings.FAQ_SETTINGS:
            return ['_description']
        else:
            return None

class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment", "question", "user", "post_time")
    list_filter = ('question', "post_time")
    search_fields = ['comment', "question"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "slug", "helpful", "not_helpful")
    list_filter = ('helpful', "not_helpful", "category")
    search_fields = ["question"]
    readonly_fields = ('helpful', "not_helpful", "slug")


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

# if category enabled
if "no_category" not in settings.FAQ_SETTINGS:
    admin.site.register(Category, CategoryAdmin)

# if comments are enabled
if "no_comments" not in settings.FAQ_SETTINGS:
    admin.site.register(FAQComment, CommentAdmin)

# if votes are enabled
if "no_votes" not in settings.FAQ_SETTINGS:
    # if answer votes are enabled
    if "no_answer_votes" not in settings.FAQ_SETTINGS:
        admin.site.register(AnswerHelpful, AnswerHelpfulAdmin)

    # if question votes are enabled
    if "no_question_votes" not in settings.FAQ_SETTINGS:
        admin.site.register(QuestionHelpful, QuestionHelpfulAdmin)
