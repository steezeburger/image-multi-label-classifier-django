from django.db import models

from common.models.crud_timestamps_mixin import CRUDTimestampsMixin
from common.models.uuid_mixin import UUIDModelMixin


class Label(UUIDModelMixin,
            CRUDTimestampsMixin):
    slug = models.CharField(
        max_length=1024,
        null=False,
        db_index=True,
        unique=True,
        help_text="The slug of the label.")

    description = models.TextField(
        null=True,
        blank=True)

    def serialized(self):
        return {
            'slug': self.slug,
            'description': self.description,
        }

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'labels'
        default_permissions = ()
        ordering = ('slug',)
        verbose_name = 'Label'
        verbose_name_plural = 'Labels'
