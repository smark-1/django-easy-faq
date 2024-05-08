from django import forms
from django.conf import settings
from . import models

class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ["answer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "rich_text_answers" in settings.FAQ_SETTINGS:
            try:
                from tinymce.widgets import TinyMCE
                self.fields["answer"].widget = TinyMCE()
            except ImportError:
                raise ImportError("Please install django-tinymce to use rich text answers")

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.FAQComment
        fields = ["comment"]


class VoteForm(forms.Form):
    vote = forms.BooleanField(label="helpful? ", required=False)
