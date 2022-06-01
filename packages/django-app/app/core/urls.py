from django.urls import path

from core.api_controllers import images_controller
from core.views import (
    HomeView,
    # LabelView,
    LabelImagesView,
)

urlpatterns = [
    path('',
         HomeView.as_view(),
         name='home'),

    # path('labels/',
    #      LabelView.as_view(),
    #      name='label-images'),

    path('label-images/<int:pk>',
         LabelImagesView.as_view(),
         name='label-images-w-pk'),
    path('label-images/',
         LabelImagesView.as_view(),
         name='label-images'),

    path('api/images/<int:id>', images_controller, name='images'),
]
