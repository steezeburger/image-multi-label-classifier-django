from django.conf import settings
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_url'] = settings.SITE_URL

        pk = kwargs.get('pk', None)
        if pk:
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

        else:
            # TODO - handle no pk. show random?
            pass

        return context
