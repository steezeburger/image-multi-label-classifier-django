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
        related_name='labeled_images',
        on_delete=models.CASCADE)

    image = models.ForeignKey(
        'core.Image',
        related_name='labeled_images',
        on_delete=models.CASCADE)

    @property
    def filename(self) -> str:
        return self.image.filename

    @property
    def title(self) -> str:
        return f'{self.label.slug}: {self.image.filename}'

    @property
    def image_tag(self) -> str:
        return self.image.image_tag

    @property
    def slug(self) -> str:
        return self.label.slug

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
        element = f'''
        <a href="/label-images/{self.pk}" target="_blank">
            <img src="{settings.MEDIA_URL}{self.uri}" width="64" height="64" />
        </a>'''
        return mark_safe(element)

    def get_previous(self) -> 'Image':
        return Image.objects.filter(
            pk__lt=self.pk).order_by('-pk').first()

    def get_next(self) -> 'Image':
        return Image.objects.filter(
            pk__gt=self.pk).order_by('pk').first()

    def has_label(self, slug: str) -> bool:
        return self.labels.filter(slug=slug).exists()

    def serialized(self) -> dict:
        return {
            'filename': self.filename,
            'uri': self.uri,
            'description': self.description,
            'labels': [l.slug for l in self.labels.all()],
        }

    def as_csv_row_w_labels(self, all_slugs: list) -> list:
        """
        Returns a list like [filename, 0, 1, ...]

        The first column is the filename.

        For each subsequent column,
        the value will be 0 if the image does not
        contain the label described by the column header,
        or 1 if the image does contain the label.
        """
        slugs_for_image = self.labels.values_list('slug', flat=True)

        result = [self.filename]
        for slug in all_slugs:
            # write a 1 or 0 depending on if the image has the label
            result.append(int(slug in slugs_for_image))

        return result

    def __str__(self) -> str:
        return self.filename

    class Meta:
        db_table = 'images'
        default_permissions = ()
        ordering = ('filename',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
