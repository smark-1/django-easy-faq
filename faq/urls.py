from django.urls import path
from . import views
from . import path_converters
from django.conf import settings

app_name = 'faq'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index_view"),
]

# if using categories
if "no_category" not in settings.FAQ_SETTINGS:
    urlpatterns += [
        path("<uslug:slug>/", views.CategoryDetail.as_view(), name="category_detail"),
        path("<uslug:slug>/add/question/", views.AddQuestion.as_view(), name="add_question"),
        path("<uslug:slug>/<uslug:question>/", views.QuestionDetail.as_view(), name="question_detail"),
        path("<uslug:category>/<uslug:question>/answer/", views.AddAnswer.as_view(), name="answer_question"),
    ]
else:
    urlpatterns += [
        path("<uslug:slug>/", views.QuestionDetail.as_view(), name="question_detail"),
        path("<uslug:question>/answer/", views.AddAnswer.as_view(), name="answer_question"),
        path("add/question", views.AddQuestion.as_view(), name="add_question"),
    ]

# if using comments
if "no_comments" not in settings.FAQ_SETTINGS:
    # if using categories
    if "no_category" not in settings.FAQ_SETTINGS:
        urlpatterns += [
            path("<uslug:category>/<uslug:question>/add/comment/", views.AddComment.as_view(), name="add_comment"),
        ]
    else:
        urlpatterns += [
            path("<uslug:question>/add/comment/", views.AddComment.as_view(), name="add_comment"),
        ]

# if using votes
if "no_votes" not in settings.FAQ_SETTINGS:
    # if using categories
    if "no_category" not in settings.FAQ_SETTINGS:
        urlpatterns += [
            path("<uslug:category>/<uslug:question>/<uslug:answer>/vote/", views.VoteAnswerHelpful.as_view(),
                 name="vote_answer"),
            path("<uslug:category>/<uslug:question>/vote/", views.VoteQuestionHelpful.as_view(), name="vote_question")
        ]
    else:
        urlpatterns += [
            path("<uslug:question>/<uslug:answer>/vote/", views.VoteAnswerHelpful.as_view(),
                 name="vote_answer"),
            path("<uslug:question>/vote/", views.VoteQuestionHelpful.as_view(), name="vote_question")
        ]
