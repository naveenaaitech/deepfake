from django.urls import path
from .views import StartAnalysisAPIView
from .views import save_detection_result

from .views import (
    VideoUploadAPIView,
    VideoResultAPIView,
    VideoHistoryAPIView,
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
    path(
        "history/",
        VideoHistoryAPIView.as_view(),
        name="video-history",
    ),
    path(
    "start/<int:pk>/",
    StartAnalysisAPIView.as_view(),
    name="start-analysis",
),
path(
    "save-result/<int:pk>/",
    save_detection_result,
    name="save-detection-result",
),
]