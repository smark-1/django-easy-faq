from django.test import TestCase, RequestFactory, override_settings
from django.shortcuts import reverse
from .views import IndexView, CategoryDetail, QuestionDetail
from . import models
from django.contrib.auth.models import User


# Create your tests here.

class IndexViewTestCase(TestCase):

    @override_settings(FAQ_SETTINGS=["no_category"])
    def test_get_template_names_no_categories(self):
        "gets correct template when not using categories"
        request = RequestFactory().get(reverse("faq:index_view"))
        view = IndexView()
        view.setup(request)

        self.assertEquals(view.get_template_names(), "faq/questions_list.html")
        self.assertNotEquals(view.get_template_names(), "faq/categories_list.html")

    @override_settings(FAQ_SETTINGS=[])
    def test_get_template_names_categories(self):
        "gets correct template when not using categories"
        request = RequestFactory().get(reverse("faq:index_view"))
        view = IndexView()
        view.setup(request)

        self.assertNotEquals(view.get_template_names(), "faq/questions_list.html")
        self.assertEquals(view.get_template_names(), "faq/categories_list.html")

    @override_settings(FAQ_SETTINGS=["no_category"])
    def test_get_queryset_no_categories(self):
        "gets correct query set when not using categories"
        request = RequestFactory().get(reverse("faq:index_view"))
        view = IndexView()
        view.setup(request)

        models.Question.objects.create(question="?")
        models.Question.objects.create(question="the?")
        view.get_queryset()

        self.assertEqual(view.get_queryset().first(), models.Question.objects.first())
        self.assertNotEqual(view.get_queryset().first(), models.Question.objects.last())
        self.assertNotEqual(view.get_queryset().first(), models.Category.objects.first())

    @override_settings(FAQ_SETTINGS=[])
    def test_get_queryset_categories(self):
        "gets correct query set when using categories"
        request = RequestFactory().get(reverse("faq:index_view"))
        view = IndexView()
        view.setup(request)

        category = models.Category.objects.create(name="category", description="this is a category")
        models.Category.objects.create(name="category 2", description="this is a category")
        models.Question.objects.create(question="category question", category=category)
        models.Question.objects.create(question="category question 2", category=category)
        models.Question.objects.create(question="question not in category")

        self.assertEqual(view.get_queryset().first(), models.Category.objects.first())
        self.assertNotEqual(view.get_queryset().first(), models.Question.objects.first())
        self.assertNotEqual(view.get_queryset().first(), models.Category.objects.last())

    @override_settings(FAQ_SETTINGS=[])
    def test_get_context_object_name_categories(self):
        "gets correct template variable when using categories"
        request = RequestFactory().get(reverse("faq:index_view"))
        view = IndexView()
        view.setup(request)

        self.assertEqual(view.get_context_object_name([]), "categories")
        self.assertNotEqual(view.get_context_object_name([]), "questions")

    @override_settings(FAQ_SETTINGS=["no_category"])
    def test_get_context_object_name_no_categories(self):
        "gets correct template variable when not using categories"
        request = RequestFactory().get(reverse("faq:index_view"))
        view = IndexView()
        view.setup(request)

        self.assertEqual(view.get_context_object_name([]), "questions")
        self.assertNotEqual(view.get_context_object_name([]), "categories")

    @override_settings(FAQ_SETTINGS=["no_category"])
    def test_get_context_data_not_using_categories(self):
        "gets context data correctly when not using categories"
        request = RequestFactory().get(reverse("faq:index_view"))
        view = IndexView()
        view.object_list = view.get_queryset()
        view.setup(request)

        self.assertIn("can_add_question", view.get_context_data())

    @override_settings(FAQ_SETTINGS=[])
    def test_get_context_data_using_categories(self):
        "gets context data correctly when using categories"
        request = RequestFactory().get(reverse("faq:index_view"))
        view = IndexView()
        view.object_list = view.get_queryset()
        view.setup(request)

        self.assertNotIn("can_add_question", view.get_context_data())

    @override_settings(FAQ_SETTINGS=["no_category", "logged_in_users_can_add_question"])
    def test_get_context_data_not_using_categories_logged_in_can_add(self):
        "gets context data correctly when not using categories and logged_in_users_can_add_question"
        request = RequestFactory()
        request = request.get(reverse("faq:index_view"))
        request.user = User.objects.create_user(username="jim", password="the")
        view = IndexView()
        view.object_list = view.get_queryset()
        view.setup(request)

        self.assertIn("can_add_question", view.get_context_data())


class CategoryDetailTestCase(TestCase):
    def setUp(self):
        models.Category.objects.create(name="cat1", description="descript")
        models.Category.objects.create(name="cat2", description="descript2")
        models.Category.objects.create(name="cat3")


class QuestionViewTestCase(TestCase):
    def setUp(self):
        category = models.Category.objects.create(name="cat1", description="descript")

        models.Question.objects.create(category=category, question="great question")

    @override_settings(FAQ_SETTINGS=[])
    def test_anonymous_user_cant_vote(self):
        """a user doesn't get a link to vote"""

        question = models.Question.objects.first()
        response = self.client.get(reverse("faq:question_detail", args=(question.category.slug, question.slug,)))

        self.assertEqual(response.context['can_vote_question'], False)
        self.assertEqual(response.context['can_vote_answer'], False)


class VoteQuestionTestCase(TestCase):
    def setUp(self):
        category = models.Category.objects.create(name="cat1", description="descript")

        models.Question.objects.create(category=category, question="great question")

    @override_settings(FAQ_SETTINGS=[])
    def test_anonymous_user_cant_vote(self):
        """redirects logged out users to login page"""

        question = models.Question.objects.first()
        response = self.client.post(reverse("faq:vote_question", args=(question.category.slug, question.slug,)))

        self.assertEqual(response.status_code, 302)


class VoteanswerTestCase(TestCase):
    def setUp(self):
        category = models.Category.objects.create(name="cat1", description="descript")

        question = models.Question.objects.create(category=category, question="great question")

        self.answer = models.Answer.objects.create(question=question, answer="because")

    @override_settings(FAQ_SETTINGS=[])
    def test_anonymous_user_cant_vote(self):
        """redirects logged out users to login page"""

        question = models.Question.objects.first()
        response = self.client.post(
            reverse("faq:vote_answer", args=(question.category.slug, question.slug, self.answer.slug)))

        self.assertEqual(response.status_code, 302)
