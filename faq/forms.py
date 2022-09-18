from django import forms
from django.conf import settings
from . import models


class CategoryForm(forms.ModelForm):
    """
    creates a form to create and update a category
    if you don't plan on using a description for your category
    then add this to the FAQ_SETTINGS dictionary inside of the settings file
    "category_description":False,
    """

    class Meta:
        model = models.Category
        fields = ["name", "slug"]

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        # if using category descriptions add to form
        if "no_category_description" not in settings.FAQ_SETTINGS:
            self.fields["description"] = forms.CharField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.FAQComment
        fields = ["comment"]


class VoteForm(forms.Form):
    vote = forms.BooleanField(label="helpful? ", required=False)
