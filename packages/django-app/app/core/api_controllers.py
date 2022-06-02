import json

from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_http_methods

from core.commands import CreateLabelCommand, UpdateImageCommand
from core.forms import CreateLabelForm, UpdateImageForm
from core.repositories import ImageRepository


@require_http_methods(['PUT'])
def images_controller(request, pk):
    """
    API Controller for updating images.
    """
    data = json.loads(request.body)

    image = ImageRepository.get(pk=pk)
    if not image:
        return HttpResponseNotFound(
            f'No image found for pk: {pk}')

    data['pk'] = pk
    form = UpdateImageForm(data)
    image = UpdateImageCommand(form).execute()
    return JsonResponse(image.serialized())


@require_http_methods(['POST'])
def labels_controller(request):
    """
    API Controller for updating an image.
    """
    data = json.loads(request.body)
    form = CreateLabelForm(data)
    label = CreateLabelCommand(form).execute()
    return JsonResponse(label.serialized())
