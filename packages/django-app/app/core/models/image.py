from django.db import models

from common.models.crud_timestamps_mixin import CRUDTimestampsMixin
from common.models.soft_delete_timestamp_mixin import SoftDeleteTimestampMixin
from common.models.uuid_mixin import UUIDModelMixin


class LabeledImage(UUIDModelMixin,
                   CRUDTimestampsMixin,
                   SoftDeleteTimestampMixin):
    label = models.ForeignKey(
        'core.Label',
        on_delete=models.CASCADE)

    image = models.ForeignKey(
        'core.Image',
        on_delete=models.CASCADE)

    @property
    def title(self):
        return f'{self.label.slug}: {self.image.filename}'

    class Meta:
        db_table = 'labeled_images'
        default_permissions = ()
        ordering = ('-id',)


class Image(UUIDModelMixin,
            CRUDTimestampsMixin,
            SoftDeleteTimestampMixin):
    filename = models.CharField(
        max_length=1024,
        null=False,
        db_index=True,
        help_text="The filename of the image.")

    uri = models.TextField(
        null=False,
        help_text="The full path of the image in the docker container.")

    description = models.TextField(
        null=True,
        blank=True)

    labels = models.ManyToManyField(
        'core.Label',
        related_name='images',
        through=LabeledImage)

    class Meta:
        db_table = 'images'
        default_permissions = ()
        ordering = ('-id',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
