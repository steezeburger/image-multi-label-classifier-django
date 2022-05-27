from common.repositories.base_repository import BaseRepository
from core.models import Label


class LabelRepository(BaseRepository):
    model = Label

    @classmethod
    def get_by_filter(cls, filter_input: dict = None):
        if filter_input:
            qs = cls.get_queryset()
            labels = qs.filter(**filter_input)
        else:
            labels = cls.get_queryset().all()
        return labels

    @classmethod
    def create(cls, data: dict) -> 'Label':
        label = cls.model.objects.create(**data)
        return label

    @classmethod
    def delete(cls, *, pk=None, obj: 'Label' = None) -> 'Label':
        label = obj or cls.get(pk=pk)
        label.delete()
        return label

    @classmethod
    def update(cls, *, pk=None, obj: 'Label' = None, data: dict) -> 'Label':
        label = obj or cls.get(pk=pk)

        if 'filename' in data:
            label.filename = data['filename']

        if 'uri' in data:
            label.uri = data['uri']

        if 'description' in data:
            label.description = data['description']

        label.save()
        return label
