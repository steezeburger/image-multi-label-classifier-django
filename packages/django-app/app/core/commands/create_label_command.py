from common.commands.abstract_base_command import AbstractBaseCommand
from core.forms import CreateLabelForm
from core.models import Label
from core.repositories import LabelRepository


class CreateLabelCommand(AbstractBaseCommand):
    """
    Command for creating a label.
    """

    def __init__(self, form: 'CreateLabelForm'):
        self.form = form

    def execute(self) -> 'Label':
        super().execute()

        label = LabelRepository.create(self.form.cleaned_data)
        return label
