import secrets
from django.conf import settings

ALL_URL_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def create_random_slug(size=10):
    """amount of characters you want generated for random_slug"""
    res = ''.join(secrets.choice(ALL_URL_CHARS) for _ in range(size))
    return str(res)


def get_template_settings(request):
    """returns most of the settings to be added into get_context_data method"""
    context = {}
    # if using categories
    if "no_category" not in settings.FAQ_SETTINGS:
        context['category_enabled'] = True
    else:
        context['category_enabled'] = False

    if "allow_multiple_answers" in settings.FAQ_SETTINGS:
        context['allow_multiple_answers'] = True
    else:
        context['allow_multiple_answers'] = False

    # if using comments
    if "no_comments" not in settings.FAQ_SETTINGS:
        context["comments_allowed"] = True
        if "anonymous_user_can_comment" in settings.FAQ_SETTINGS:
            context['add_new_comment_allowed'] = True
        else:
            if request.user.is_authenticated:
                context['add_new_comment_allowed'] = True
            else:
                context['add_new_comment_allowed'] = False

        if "view_only_comments" in settings.FAQ_SETTINGS:
            context['add_new_comment_allowed'] = False
    else:
        context["comments_allowed"] = False

    # if can vote on answers
    if "no_votes" not in settings.FAQ_SETTINGS:
        # if can vote answer
        if "no_answer_votes" not in settings.FAQ_SETTINGS:
            if request.user.is_authenticated:
                context["can_vote_answer"] = True
            else:
                context["can_vote_answer"] = False
        else:

            context["can_vote_answer"] = False

        if "no_question_votes" not in settings.FAQ_SETTINGS:
            if request.user.is_authenticated:
                context["can_vote_question"] = True
            else:
                context["can_vote_question"] = False
        else:

            context["can_vote_question"] = False
    else:
        context["can_vote_answer"] = False
        context["can_vote_question"] = False

    context["can_add_question"] = False
    if "logged_in_users_can_add_question" in settings.FAQ_SETTINGS:
        if request.user.is_authenticated:
            context["can_add_question"] = True

    return context
