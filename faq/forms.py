from django import forms
from . import models


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.FAQComment
        fields = ["comment"]


class VoteForm(forms.Form):
    vote = forms.BooleanField(label="helpful? ", required=False)
