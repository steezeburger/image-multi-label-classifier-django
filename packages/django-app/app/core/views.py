from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from core.repositories import LabelRepository, ImageRepository


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = LabelRepository.get_by_filter()
        return context


# class LabelView(TemplateView):
#     template_name = 'core/labels.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['img_src'] = ''
#         return context


class LabelImagesView(TemplateView):
    template_name = 'core/label-images.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            redirect_to_pk = ImageRepository.get_by_filter().first().pk
            return HttpResponseRedirect(
                reverse_lazy('label-images-w-pk',
                             kwargs={'pk': redirect_to_pk}))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_url'] = settings.SITE_URL

        context['total_images_count'] = ImageRepository.get_by_filter().count() * .1
        context['labeled_images_count'] = ImageRepository.get_by_filter({'labels__isnull': False}).count()

        pk = kwargs.get('pk', None)
        image = ImageRepository.get(pk=pk)

        # TODO - pretty errors
        if not image:
            raise NotImplementedError

        context['img_uri'] = image.uri
        context['current_image_pk'] = image.pk

        selected_labels = image.labels.all()
        selected_labels_slugs = [l.slug for l in selected_labels]
        context['labels'] = [
            {
                "slug": label.slug,
                "is_selected": label.slug in selected_labels_slugs,
            } for label in LabelRepository.get_by_filter()
        ]

        context['random_pk'] = ImageRepository.get_random().pk

        previous_image = image.get_previous()
        if previous_image:
            context['previous_pk'] = previous_image.pk

        next_image = image.get_next()
        if next_image:
            context['next_pk'] = next_image.pk

        return context
