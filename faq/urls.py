from django.urls import path
from . import views
from django.conf import settings

app_name = 'faq'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index_view"),
]

# if using categories
if "no_category" not in settings.FAQ_SETTINGS:
    urlpatterns += [
        path("<slug:slug>/", views.CategoryDetail.as_view(), name="category_detail"),
        path("<slug:slug>/add/question/", views.AddQuestion.as_view(), name="add_question"),
        path("<slug:slug>/<slug:question>/", views.QuestionDetail.as_view(), name="question_detail"),
        path("<slug:category>/<slug:question>/answer/", views.AddAnswer.as_view(), name="answer_question"),
    ]
else:
    urlpatterns += [
        path("<slug:slug>/", views.QuestionDetail.as_view(), name="question_detail"),
        path("<slug:question>/answer/", views.AddAnswer.as_view(), name="answer_question"),
        path("add/question", views.AddQuestion.as_view(), name="add_question"),
    ]

# if using comments
if "no_comments" not in settings.FAQ_SETTINGS:
    # if using categories
    if "no_category" not in settings.FAQ_SETTINGS:
        urlpatterns += [
            path("<slug:category>/<slug:question>/add/comment/", views.AddComment.as_view(), name="add_comment"),
        ]
    else:
        urlpatterns += [
            path("<slug:question>/add/comment/", views.AddComment.as_view(), name="add_comment"),
        ]

# if using votes
if "no_votes" not in settings.FAQ_SETTINGS:
    # if using categories
    if "no_category" not in settings.FAQ_SETTINGS:
        urlpatterns += [
            path("<slug:category>/<slug:question>/<slug:answer>/vote/", views.VoteAnswerHelpful.as_view(),
                 name="vote_answer"),
            path("<slug:category>/<slug:question>/vote/", views.VoteQuestionHelpful.as_view(), name="vote_question")
        ]
    else:
        urlpatterns += [
            path("<slug:question>/<slug:answer>/vote/", views.VoteAnswerHelpful.as_view(),
                 name="vote_answer"),
            path("<slug:question>/vote/", views.VoteQuestionHelpful.as_view(), name="vote_question")
        ]
