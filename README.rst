========
easy-faq
========

easy-faq is a Django app to allow for a simple yet feature rich faq app. with categories, commenting voting of questions and answers all as an optional part of the app.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "easy-faq" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'faq',
    ]

2. Include the easy-faq URLconf in your project urls.py like this::

    path('faq/', include('faq.urls')),

3. Run ``python manage.py migrate`` to create the faq models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a category (you'll need the Admin app enabled).(categories part of the app can be disabled)

5. Visit http://127.0.0.1:8000/faq/ to see the categories.