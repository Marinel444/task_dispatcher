from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, WorkerViewSet, TaskStatusAPIView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"workers", WorkerViewSet, basename="worker")

urlpatterns = [
    path('', include(router.urls)),
    path('task-status/', TaskStatusAPIView.as_view()),

    # OpenAPI schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
]