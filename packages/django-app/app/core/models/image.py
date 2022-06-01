from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe

from common.models.crud_timestamps_mixin import CRUDTimestampsMixin
from common.models.soft_delete_timestamp_mixin import SoftDeleteTimestampMixin
from common.models.uuid_mixin import UUIDModelMixin


class LabeledImage(UUIDModelMixin,
                   CRUDTimestampsMixin):
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
        unique=True,
        help_text="The filename of the image.")

    uri = models.TextField(
        null=False,
        help_text="The path of the image relative to manage.py.")

    description = models.TextField(
        null=True,
        blank=True)

    labels = models.ManyToManyField(
        'core.Label',
        related_name='images',
        through=LabeledImage)

    @property
    def image_tag(self) -> str:
        element = f'<img src="{settings.MEDIA_URL}{self.uri}" width="64" height="64" />'
        return mark_safe(element)

    def get_previous(self) -> 'Image':
        return Image.objects.filter(
            pk__lt=self.pk).order_by('-pk').first()

    def get_next(self) -> 'Image':
        return Image.objects.filter(
            pk__gt=self.pk).order_by('pk').first()

    def has_label(self, slug: str) -> bool:
        return self.labels.filter(slug=slug).exists()

    def serialized(self):
        return {
            'filename': self.filename,
            'uri': self.uri,
            'description': self.description,
            'labels': [l.slug for l in self.labels.all()],
        }

    def __str__(self):
        return self.filename

    class Meta:
        db_table = 'images'
        default_permissions = ()
        ordering = ('filename',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
