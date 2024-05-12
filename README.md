# django-easy-faq

django-easy-faq is a Django app to allow for a simple yet feature rich faq app. with categories, commenting voting of questions and answers all as an optional part of the app. To see screenshots of what this django-easy-faq could look like with bootstrap 5 styling [click here](demo/demo.md).


## Quick start

1. pip install:

    `pip install django-easy-faq`

2. Add "faq" to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = [
        ...
        'faq',]
    ```

3. Include the easy-faq URLconf in your project urls.py like this::

    ```python
    #…
    path('faq/', include('faq.urls')),
    #…
    ```

4. Add `FAQ_SETTINGS = []` to your `settings.py`
5. Run ``python manage.py makemigrations`` to create the faq models migrations.
6. Run ``python manage.py migrate`` to create the faq models.

7. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a category (you'll need the Admin app enabled).(categories part of the app can be disabled)

8. Visit http://127.0.0.1:8000/faq/ to see the categories.

## Settings

you can change most things in settings below is a list of all settings
add any or all to change to desired behavior::


    FAQ_SETTINGS = ['your_settings_here',]


1. no_category_description                  - add if using categories but don't want descriptions for them
2. no_category                              - add if don't want to use categories
3. logged_in_users_can_add_question         - add if you want any logged in user to be able to ask a question
4. logged_in_users_can_answer_question      - add if you want any logged in user to be able to answer a question
5. allow_multiple_answers                   - add if you want a question to be able to be answered multiple times
6. no_comments                              - add if don't want to use comments
7. anonymous_user_can_comment               - add if you want any user to be able to comment including anonymous users
8. view_only_comments                       - add if you want users to see posted comments but not be able to add any more
9. no_votes                                 - add if don't want any voting for useful questions or answers
10. no_answer_votes                         - add if only want question voting
11. no_question_votes                       - add if only want answer voting
12. allow_unicode                           - add if you want to allow unicode slugs
13. login_required                          - add if you want to only let logged in users see FAQ's
14. rich_text_answers                       - add if you want to use rich text for answers. This requires the django-tinymce package to be installed

## Templates

all of the templates are meant to be overwritten
to overwrite them create a faq directory inside of the templates directory and add a html file with the same name to it

if this doesn't work make sure that the templates setting has 'DIRS': ['templates'], in it::

    TEMPLATES = [
        {
            ...
            'DIRS': ['templates'],
            ...
        },
    ]

here is a list of templates and there default template  you can overwrite

1. categories_list.html - faq main view if using categories::


        <h1>select a FAQ category</h1>
        {% for category in categories %}
            <h3><a href="{% url 'faq:category_detail' category.slug %}">{{category.name}}</a></h3>
            {% if category.description %}
                <p>{{category.description}}</p>
            {% endif %}
            <hr>
        {% endfor %}


2. category_detail.html - faq category detail view if using categories::


        <h1>choose a FAQ Question</h1>
        <h2>{{category}}</h2>
        {% if category.description %}
        <p>{{category.description}}</p>
        {% endif %}
        <hr>
        {% for question in category.question_set.all %}
            <h3><a href="{% url 'faq:question_detail' category.slug question.slug %}">{{question.question}}</a></h3>
        {% endfor %}
        <hr>
        <a href="{% url 'faq:index_view' %}">back</a>
        {% if can_add_question %}
            <a href="{% url 'faq:add_question' category.slug %}">add question</a>
        {% endif %}


3. questions_list.html - lists all questions if not using categories::


        <h1>choose a FAQ Question</h1>
        {% for question in questions %}
            <h3><a href="{% url 'faq:question_detail' question.slug %}">{{question.question}}</a></h3>
        {% endfor %}
    
        {% if can_add_question %}
            <hr>
            <a href="{% url 'faq:add_question' %}">add question</a>
        {% endif %}


4. question_detail.html - the question detail page::


        {% extends 'faq/question_base.html' %}
    
        {% block question_content %}
        {% if allow_multiple_answers %}
        <h3>answers</h3>
        <ul>
            {% for answer in question.answer_set.all %}
                <li><b>{{answer.answer}}</b>
                    {% if can_vote_answer %}
                     | found this answer helpful?
                    <form style="display: inline;" action="{% if category_enabled %}{% url 'faq:vote_answer' question.category.slug question.slug answer.slug %}{% else %}{% url 'faq:vote_answer' question.slug answer.slug %}{% endif %}" method="post">
                        {% csrf_token %}
                        <input type="hidden" value=True name="vote">
                        <button type="submit">yes({{answer.helpful}})</button>
                    </form>
                    <form style="display: inline;" action="{% if category_enabled %}{% url 'faq:vote_answer' question.category.slug question.slug answer.slug %}{% else %}{% url 'faq:vote_answer' question.slug answer.slug %}{% endif %}" method="post">
                        {% csrf_token %}
                        <input type="hidden" value=False name="vote">
                        <button type="submit">no({{answer.not_helpful}})</button>
                    </form>
                    {% endif %}
                </li>
            {% endfor %}
        </ul>
    
        {% else %}
            {% if question.answer_set.exists %}
                <p>answer:</p>
                <h3>{{question.answer_set.first.answer}}</h3>
                {% if can_vote_answer %}
                 found this answer helpful?
                <form style="display: inline;" action="{% if category_enabled %}{% url 'faq:vote_answer' question.category.slug question.slug question.answer_set.first.slug %}{% else %}{% url 'faq:vote_answer' question.slug question.answer_set.first.slug %}{% endif %}" method="post">
                    {% csrf_token %}
                    <input type="hidden" value=True name="vote">
                    <button type="submit">yes({{question.answer_set.first.helpful}})</button>
                </form>
                <form style="display: inline;" action="{% if category_enabled %}{% url 'faq:vote_answer' question.category.slug question.slug question.answer_set.first.slug %}{% else %}{% url 'faq:vote_answer' question.slug question.answer_set.first.slug %}{% endif %}" method="post">
                    {% csrf_token %}
                    <input type="hidden" value=False name="vote">
                    <button type="submit">no({{question.answer_set.first.not_helpful}})</button>
                </form>
                {% endif %}
            {% else %}
                no answers yet
            {% endif %}
        {% endif %}
    
    
        {% if can_answer_question %}
            {% if category_enabled %}
                <a href="{% url 'faq:answer_question' question.category.slug question.slug %}">answer question</a>
            {% else %}
                <a href="{% url 'faq:answer_question' question.slug %}">answer question</a>
            {% endif %}
        {% endif %}
        <hr>
        {% if comments_allowed %}
            {% include 'faq/comments.html' %}
        {% endif %}
    
        {% endblock %}

5. answer_form.html - form to add answer to question::


        <h1>Answer Question</h1>
        <a href="{{question.get_absolute_url}}"><h3>{{question.question}}</h3></a>
        <form method="post">
            {% csrf_token %}
            {{form}}
            <input type="submit">
        </form>

6. comment_form.html - form to add comments to question (only shows up when form has error because view only gets posted to)::


        <h1>Post A Comment</h1>
        <a href="{{question.get_absolute_url}}"><h3>{{question.question}}</h3></a>
        <form method="post">
            {% csrf_token %}
            {{form}}
            <input type="submit">
        </form>

7. question_form.html - form to add a new question::


        <h1>Add Your Question</h1>
        <form method="post">
            {% csrf_token %}
            {{form}}
            <input type="submit">
        </form>

8. vote_form.html - form for voting questions and answers (only shows up when form has error because view only gets posted to)::


        <h1>vote</h1>
        <form method="post">
            {% csrf_token %}
            {{form}}
            <input type="submit">
        </form>

9. comments.html - if comments are allowed this template is included in the question detail.html::


        <h3>comments</h3>
        <ul>
            {% for comment in question.faqcomment_set.all %}
                <li><h4>{{comment.comment}}</h4>
                    posted by {% if comment.user%}{{comment.user}}{% else %}anonymous{% endif %} {{comment.post_time|timesince}} ago</li>
            {% endfor %}
        </ul>
        {% if add_new_comment_allowed %}
            {% if category_enabled %}
            <form method="post" action="{% url 'faq:add_comment' question.category.slug question.slug %}">
            {% else %}
            <form method="post" action="{% url 'faq:add_comment' question.slug %}">
            {% endif %}
            <fieldset>
                <legend>Post Your Comment Here:</legend>
                {% csrf_token %}
                {{comment_form}}
                <input type="submit" name="post">
            </fieldset>
            </form>
        {% endif %}

## Template Variables

1. categories_list.html
    categories - all the categories (category queryset)

2. categories_detail.html
    category - the category chosen (category object)
    can_add_question - bool if the user can add a question (depends on the settings)
3. questions_list.html
    questions - all the questions (question queryset)
    can_add_question - bool if the user can add a question (depends on the settings)
4. question_detail.html
    question - the question chosen (question object)
    can_vote_question - bool if the user can vote a question (depends on the settings)
    category_enabled - bool if category enabled in settings
    allow_multiple_answers - bool if multiple answers allowed in settings
    can_vote_answer - bool if the user can vote an answer (depends on the settings)
    can_answer_question - bool if current user can answer question (depends on the settings)
    comments_allowed - bool if using comments in settings
    add_new_comment_allowed - bool if current user can add comment (depends on the settings)
    comment_form - form to submit a new comment
5. answer_form.html
    question - the question to add answer to (question object)
    form - form to add new answer
6. comment_form.html
    question - the question to add comment to (question object)
    form - form to add new comment
7. question_form.html
    form - form to add new question
8. vote_form.html
    form - form to vote for a question or answer

## Urls

all of the following urls are by name then additional
the app name for the urls is ``'faq'``

* index_view
    * no arguments
    * displays all the categories if categories are enabled otherwise shows questions
* category_detail
    * needs category slug as slug
    * displays all the questions given the category when categories are enabled
* add_question
    * if categories are enabled needs category slug as slug
    * if logged_in_users_can_add_question then displays form for logged in users to ask a new question
* question_detail
    * needs question slug as question | if categories are enabled needs category slug as slug
    * displays the main FAQ page with the question all the comments and answers
* answer_question
    * needs question slug as question | if categories are enabled needs category slug as category
    * displays the answer question form
* add_comment
    * needs question slug as question | if categories are enabled needs category slug as category
    * only works if using comments
    * used to post comment form from question_detail to database
* vote_answer
    * needs question slug as question | needs answer slug as answer | if categories are enabled needs category slug as category
    * only works if using answer voting
    * used to post hidden input vote = 1 or vote = 0 depending on vote up or down
* vote_question
    * needs question slug as question | if categories are enabled needs category slug as category
    * only works if using question voting
    * used to post hidden input vote = 1 or vote = 0 depending on vote up or down

## django-tinymce
If you want to use rich text answers you will need to [install django-tinymce](https://django-tinymce.readthedocs.io/en/latest/installation.html#id2)

Make sure to include in the template the `{{ form.media }}` to include the tinymce javascript and css files.
> [!WARNING]  
> Failing to follow the following steps will result in a xss vulnerability in your site.

To allow the rich text answers to be rendered properly you will need to use the safe filter in your templates.
While django-tinymce does escape the html the answers that were created when the rich text editor was not enabled **has not been escaped and is not safe**.
So these answers cannot be rendered with the safe filter. So a flag was added to the answer model 'is_rich_text' that is set to True when the answer is created with the rich text editor.
In the template you can use the following code to render the answer properly::

    {% if answer.is_rich_text %}
        {{answer.answer|safe}}
    {% else %}
        {{answer.answer}}
    {% endif %}

## Contributing

django-easy-faq aims to be the best faq app for django. It welcomes  contributions of all types - issues, bugs, feature requests, documentation updates, tests and pull requests

## change log
0.4 fixed bug that logged out users can vote - which then raises exceptions

0.5 fixed migrations

1.0 added pypi distribution

1.1 added more templates to override easily

1.2 fixed bug in pypi distro not including faq app

1.3 fixed bug where a slug must be filled out in admin even though slug gets auto generated to save for questions, answers, and categories. Made questions, answers, categories slugs readonly in admin

1.4 added unicode option to add unicode slugs

1.5 added login_required setting to allow faq app to be available to only logged in users

1.6 fixed bug where no_category_description did not do remove the category description in the admin

1.7 added support for django 5.0

1.8 added support for richtext answers with django-tinymce

1.9 added view onsite link in admin, added richtext answers in admin
