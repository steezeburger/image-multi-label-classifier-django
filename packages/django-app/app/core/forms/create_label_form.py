from django import forms

from common.forms.base_form import BaseForm


class CreateLabelForm(BaseForm):
    slug = forms.CharField(
        max_length=255,
        required=True)
