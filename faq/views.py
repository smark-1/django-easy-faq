from django.core.exceptions import PermissionDenied
from django.shortcuts import reverse
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
from . import models
from . import forms
from .snippets import get_template_settings


# Create your views here.
class IndexView(generic.ListView):
    """
    this view depending on settings either displays all the categories as a list if the categories is enabled using the categories_list.html template

    if categories are not enabled it will then show a list of all the questions using questions_list.html template
    """

    def get_template_names(self):
        """if "no_category" render questions_list.html
            else render categories_list.html"""
        if "no_category" in settings.FAQ_SETTINGS:
            return "faq/questions_list.html"
        return "faq/categories_list.html"

    def get_queryset(self):
        if "no_category" in settings.FAQ_SETTINGS:
            return models.Question.objects.all()
        return models.Category.objects.all()

    def get_context_object_name(self, object_list):
        if "no_category" in settings.FAQ_SETTINGS:
            return "questions"
        return "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_template_settings(self.request))  # add in all settings into templates
        return context


class CategoryDetail(generic.DetailView):
    """
    this view only runs when categories are enabled
    this view shows all the questions related to this category
    """
    model = models.Category
    template_name = "faq/category_detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update(get_template_settings(self.request))  # add in all settings into templates
        return context


class AddQuestion(UserPassesTestMixin, generic.CreateView):
    """
    this view is for a user to add a question to the faq questions
    if the using categories then this will also add the current category to it
    the default setting is only to allow the superuser to add new questions
    to change this:
        A) override the testfunc method
        B) set staff_can_add_question in the FAQ_SETTINGS to True (allows any staff user to add a question)
        C) set authenticated_user_can_add_question in the FAQ_SETTINGS to True (allows any authenticated user to add a question)
    """
    model = models.Question
    fields = ['question']

    def test_func(self):
        # when authenticated_user_can_add_question in the FAQ_SETTINGS is set to True
        if "logged_in_users_can_add_question" in settings.FAQ_SETTINGS:
            if self.request.user.is_authenticated:
                return True
        return False

    def get_success_url(self):
        return self.question_url

    def form_valid(self, form):
        # if using categories
        if "no_category" not in settings.FAQ_SETTINGS:
            form = form.save(commit=False)
            form.category = models.Category.objects.get(slug=self.kwargs["slug"])
            form.save()
            self.question_url = form.get_absolute_url()
            return super().form_valid(form)
        else:
            form = form.save()
            self.question_url = form.get_absolute_url()
            return super().form_valid(form)


class QuestionDetail(generic.DetailView):
    model = models.Question
    template_name = "faq/question_detail.html"
    context_object_name = "question"

    def get_object(self, queryset=None):
        # if using categories
        if "no_category" not in settings.FAQ_SETTINGS:
            return self.model.objects.get(category__slug=self.kwargs["slug"], slug=self.kwargs["question"])
        else:
            return self.model.objects.get(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(get_template_settings(self.request))  # add in all settings into templates

        # check if logged in users are allowed to answer questions
        if "logged_in_users_can_answer_question" in settings.FAQ_SETTINGS:
            # check if user is logged in
            if self.request.user.is_authenticated:
                if "allow_multiple_answers" in settings.FAQ_SETTINGS:
                    context['can_answer_question'] = True
                else:
                    # if there is already one answer
                    if self.get_object().answer_set.count() > 0:
                        context['can_answer_question'] = False
                    else:
                        context['can_answer_question'] = True
            else:
                context['can_answer_question'] = False
        else:
            context['can_answer_question'] = False

        context["comment_form"] = forms.CommentForm()
        return context


class AddAnswer(UserPassesTestMixin, generic.CreateView):
    model = models.Answer
    fields = ["answer"]
    template_name = "faq/answer_form.html"

    def test_func(self):
        # when authenticated_user_can_add_question in the FAQ_SETTINGS is set to True
        if "logged_in_users_can_answer_question" in settings.FAQ_SETTINGS:
            if self.request.user.is_authenticated:
                if "allow_multiple_answers" in settings.FAQ_SETTINGS:
                    return True
                else:

                    # if using categories
                    if "no_category" not in settings.FAQ_SETTINGS:
                        question = models.Question.objects.get(category__slug=self.kwargs['category'],
                                                               slug=self.kwargs['question'])
                    else:
                        question = models.Question.objects.get(slug=self.kwargs['question'])

                    # if there is already one answer don't allow user to add answer
                    if question.answer_set.count() > 0:
                        return False
                    else:
                        return True
        return False

    def get_success_url(self):
        # if using categories
        if "no_category" not in settings.FAQ_SETTINGS:
            return reverse("faq:question_detail", args=(self.kwargs['category'], self.kwargs['question']))
        else:
            return reverse("faq:question_detail", args=(self.kwargs['question'],))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(get_template_settings(self.request))  # add in all settings into templates

        # if using categories
        if "no_category" not in settings.FAQ_SETTINGS:
            question = models.Question.objects.get(category__slug=self.kwargs['category'], slug=self.kwargs['question'])
        else:
            question = models.Question.objects.get(slug=self.kwargs['question'])

        context["question"] = question
        return context

    def form_valid(self, form):
        form = form.save(commit=False)

        # if using categories
        if "no_category" not in settings.FAQ_SETTINGS:
            question = models.Question.objects.get(category__slug=self.kwargs['category'], slug=self.kwargs['question'])
        else:
            question = models.Question.objects.get(slug=self.kwargs['question'])

        form.question = question
        form.save()
        return super().form_valid(form)


class AddComment(generic.CreateView):
    model = models.FAQComment
    form_class = forms.CommentForm
    template_name = "faq/comment_form.html"

    def get_question(self):
        # if using categories
        if "no_category" not in settings.FAQ_SETTINGS:
            question = models.Question.objects.get(category__slug=self.kwargs['category'], slug=self.kwargs['question'])
        else:
            question = models.Question.objects.get(slug=self.kwargs['question'])

        return question

    def get_success_url(self):
        return self.get_question().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(get_template_settings(self.request))  # add in all settings into templates
        context["question"] = self.get_question()
        return context

    def form_valid(self, form):
        form = form.save(commit=False)
        form.question = self.get_question()
        if self.request.user.is_authenticated:
            form.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if "view_only_comments" in settings.FAQ_SETTINGS:
            raise PermissionDenied("comments are view only at this time")
        if self.request.user.is_authenticated:
            pass
        else:
            if not "anonymous_user_can_comment" in settings.FAQ_SETTINGS:
                raise PermissionDenied("have to be logged in to comment")
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if "view_only_comments" in settings.FAQ_SETTINGS:
            raise PermissionDenied("comments are view only at this time")
        if self.request.user.is_authenticated:
            pass
        else:
            if not "anonymous_user_can_comment" in settings.FAQ_SETTINGS:
                raise PermissionDenied("have to be logged in to comment")
        return super().post(*args, **kwargs)


class VoteAnswerHelpful(UserPassesTestMixin, generic.FormView):
    form_class = forms.VoteForm
    template_name = "faq/vote_form.html"

    def get_success_url(self):
        return self.get_question().get_absolute_url()

    def get_question(self):
        # if using categories
        if "no_category" not in settings.FAQ_SETTINGS:
            question = models.Question.objects.get(category__slug=self.kwargs['category'], slug=self.kwargs['question'])
        else:
            question = models.Question.objects.get(slug=self.kwargs['question'])

        return question

    def get_answer(self):
        return models.Answer.objects.get(question=self.get_question(), slug=self.kwargs['answer'])

    def form_valid(self, form):
        # if already voted get vote otherwise create it
        if models.AnswerHelpful.objects.filter(answer=self.get_answer(), user=self.request.user).exists():
            helpful = models.AnswerHelpful.objects.get(answer=self.get_answer(), user=self.request.user)
        else:
            helpful = models.AnswerHelpful(answer=self.get_answer(), user=self.request.user)

        helpful.vote = form.cleaned_data['vote']
        helpful.save()
        self.get_answer().save()
        return super().form_valid(form)

    def test_func(self):
        if "no_answer_votes" in settings.FAQ_SETTINGS:
            return False
        elif "no_votes" in settings.FAQ_SETTINGS:
            return False
        if not self.request.user.is_authenticated:
            return False
        return True


class VoteQuestionHelpful(UserPassesTestMixin, generic.FormView):
    form_class = forms.VoteForm
    template_name = "faq/vote_form.html"

    def get_success_url(self):
        return self.get_question().get_absolute_url()

    def get_question(self):
        # if using categories
        if "no_category" not in settings.FAQ_SETTINGS:
            question = models.Question.objects.get(category__slug=self.kwargs['category'], slug=self.kwargs['question'])
        else:
            question = models.Question.objects.get(slug=self.kwargs['question'])

        return question

    def form_valid(self, form):
        # if already voted get vote otherwise create it
        if models.QuestionHelpful.objects.filter(question=self.get_question(), user=self.request.user).exists():
            helpful = models.QuestionHelpful.objects.get(question=self.get_question(), user=self.request.user)
        else:
            helpful = models.QuestionHelpful(question=self.get_question(), user=self.request.user)

        helpful.vote = form.cleaned_data['vote']
        helpful.save()
        self.get_question().save()
        return super().form_valid(form)

    def test_func(self):
        if "no_question_votes" in settings.FAQ_SETTINGS:
            return False
        elif "no_votes" in settings.FAQ_SETTINGS:
            return False
        if not self.request.user.is_authenticated:
            return False
        return True
