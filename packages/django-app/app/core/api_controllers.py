import json

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_http_methods

from core.repositories import ImageRepository, LabelRepository


@require_http_methods(['POST', 'PUT'])
def images_controller(request, id):
    data = json.loads(request.body)

    image = ImageRepository.get(pk=id)
    if not image:
        return HttpResponseNotFound(
            f'No image found for pk: {id}')

    if 'labels' in data:
        data['labels'] = LabelRepository.get_by_filter(
            {'slug__in': data['labels']})

    image = ImageRepository.update(pk=id, data=data)

    return JsonResponse(image.serialized())
