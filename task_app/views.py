from django.db.models import Count, Q, F
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, Worker
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskStatusUpdateSerializer,
    WorkerSerializer,
    WorkerUpdateSerializer,
)


class TaskViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Task.objects.select_related("worker").all()

    def get_serializer_class(self):
        if self.action == "create":
            return TaskCreateSerializer
        if self.action == "update_status":
            return TaskStatusUpdateSerializer
        return TaskSerializer

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        task = self.get_object()
        serializer = TaskStatusUpdateSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)


class WorkerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    def get_queryset(self):
        return Worker.objects.annotate(
            active_tasks_count=Count(
                "tasks",
                filter=Q(tasks__status__in=["pending", "in_progress"])
            )
        )

    def get_serializer_class(self):
        if self.action == "update_max":
            return WorkerUpdateSerializer
        return WorkerSerializer

    @action(detail=True, methods=["patch"], url_path="max-tasks")
    def update_max(self, request, pk=None):
        worker = self.get_object()
        serializer = WorkerUpdateSerializer(worker, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(WorkerSerializer(worker).data)

    @action(detail=True, methods=["get"], url_path="tasks")
    def worker_tasks(self, request, pk=None):
        worker = self.get_object()
        tasks = worker.tasks.all().order_by("-created_at")
        return Response(TaskSerializer(tasks, many=True).data)


class TaskStatusAPIView(APIView):
    def get(self, request, *args, **kwargs):
        total = Task.objects.count()
        by_status = (
            Task.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )
        by_worker = (
            Worker.objects.annotate(
                active_tasks=Count(
                    "tasks",
                    filter=Q(tasks__status__in=["pending", "in_progress"])
                ),
                completed_tasks=Count(
                    "tasks",
                    filter=Q(tasks__status="completed")
                ),
            )
        )

        return Response({
            "total_tasks": total,
            "tasks_by_status": list(by_status),
            "workers": [
                {
                    "id": w.id,
                    "name": w.name,
                    "max_tasks": w.max_tasks,
                    "is_active": w.is_active,
                    "active_tasks": w.active_tasks,
                    "completed_tasks": w.completed_tasks,
                }
                for w in by_worker
            ]
        })
