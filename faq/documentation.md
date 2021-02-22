<h1>Documentation for django faq app</h1>
<p>this app was created so that a website can have a faq app set up and running very fast very simple
no matter your use case.
</p>
<h2>Quickstart</h2>
<h4>installation</h4>
<code>pip install django-easy-faq</code>
<p>in settings.py add <code>"faq",</code> to installed apps</p>
<h4>add the urls</h4>
<p>in urls.py add <code>path("faq/",include("faq.urls")),</code></p>
<p>the templates included are only meant to be used as a guide for what to put on which template</p>
<p>to override the template add a template with the same name to your templates directory inside a folder called "faq".</p>
<p>the names of the templates are specified in the detailed documentations views section</p>
<h4>set up data base</h4>
<p>run the following commands</p>
<ul>
<li><code>python manage.py makemigrations</code></li>
<li><code>python manage.py migrate</code></li>
</ul>
<h5>you are now finished the quick start</h5>
<p>if you want to change how anything works see the full documentation as their are a ton of customizations that you can do </p>
<h4>some of the many settings you can and might want to change</h4>
<ul>
    <li>use the categories or not</li>
    <li>use category descriptions or not</li>
    <li>who can add a category (superusers,staff,logged in user)</li>
</ul>

<h2>Categories</h2>
<h4>disabling categories</h4>
<p>
The categories will then show up on the main view with links to the category detail page with all the questions related to that category displayed on that page. 
you can remove the categories all together by adding to settings:
 
    FAQ_SETTINGS={
        "use_category":False,
    }
this will then make all the questions show up on the main view with links to the question page.
</p>
<h4>disabling category descriptions</h4>
to disable category descriptions add to settings:

    FAQ_SETTINGS={
        "category_description":False,
    }
category descriptions will no longer show up in the forms to add or edit a category
<h4>who can add and update categories</h4>
this is not for django admin this is for additional views in the faq app
<p>the super user can always add and update categories</p>
to allow staff to add and update categories add to settings:

    FAQ_SETTINGS={
        "staff_can_add_category":True,
    }

to allow any logged in user to add and update categories add to settings:

    FAQ_SETTINGS={
        "authenticated_user_can_add_category":True,
    }

<h2>template overriding</h2>
the templates included are only meant to be used as a guide for what to put on which template
<h4>home template</h4>
if you are using categories the home template is:
<code>faq/categories_list.html</code>

use <code>categories</code> as the template variable

if not using categories then the template is:
<code>faq/questions_list.html</code>

use <code>questions</code> as the template variable
<h4>category update/create</h4>
<code>faq/categories_form.html</code>