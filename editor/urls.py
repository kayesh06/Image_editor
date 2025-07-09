from django.urls import path
from .views import image_editor

urlpatterns = [
    path('', image_editor, name='image_editor'),
]