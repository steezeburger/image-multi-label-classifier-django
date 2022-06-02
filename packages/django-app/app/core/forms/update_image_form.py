from django import forms

from common.forms.base_form import BaseForm
from core.repositories import ImageRepository, LabelRepository


class UpdateImageForm(BaseForm):
    pk = forms.ModelChoiceField(
        queryset=ImageRepository.get_queryset())

    labels = forms.ModelMultipleChoiceField(
        queryset=LabelRepository.get_queryset(),
        to_field_name='slug',
        required=False)
