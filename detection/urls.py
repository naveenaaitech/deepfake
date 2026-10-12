from django.urls import path
from .views import (
    VideoUploadAPIView,
    VideoResultAPIView,
)

urlpatterns = [
    path(
        "upload/",
        VideoUploadAPIView.as_view(),
        name="video-upload",
    ),
    path(
        "result/<int:pk>/",
        VideoResultAPIView.as_view(),
        name="video-result",
    ),
]