from common.repositories.base_repository import BaseRepository
from core.models import Image


class ImageRepository(BaseRepository):
    model = Image

    @classmethod
    def get_by_filter(cls, filter_input: dict = None):
        if filter_input:
            qs = cls.get_queryset()
            images = qs.filter(**filter_input)
        else:
            images = cls.get_queryset().all()
        return images

    @classmethod
    def get_random(cls) -> 'Image':
        return cls.model.objects.order_by('?').first()

    @classmethod
    def create(cls, data: dict) -> 'Image':
        image = cls.model.objects.create(**data)
        return image

    @classmethod
    def delete(cls, *, pk=None, obj: 'Image' = None) -> 'Image':
        image = obj or cls.get(pk=pk)
        image.delete()
        return image

    @classmethod
    def update(cls, *, pk=None, obj: 'Image' = None, data: dict) -> 'Image':
        image = obj or cls.get(pk=pk)

        if 'filename' in data:
            image.filename = data['filename']

        if 'uri' in data:
            image.uri = data['uri']

        if 'description' in data:
            image.description = data['description']

        if 'labels' in data:
            image.labels.set(data['labels'])

        image.save()
        return image
