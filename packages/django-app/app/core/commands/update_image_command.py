from common.commands.abstract_base_command import AbstractBaseCommand
from core.forms import UpdateImageForm
from core.models import Image
from core.repositories import ImageRepository


class UpdateImageCommand(AbstractBaseCommand):
    """
    Command for adding labels to an image.
    """

    def __init__(self, form: 'UpdateImageForm'):
        self.form = form

    def execute(self) -> 'Image':
        super().execute()

        image = ImageRepository.update(obj=self.form.cleaned_data['pk'],
                                       data=self.form.cleaned_data)
        return image
