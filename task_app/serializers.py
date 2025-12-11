from rest_framework import serializers
from .models import Task, Worker, task_status


class WorkerSerializer(serializers.ModelSerializer):
    active_tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Worker
        fields = [
            "id",
            "name",
            "max_tasks",
            "is_active",
            "created_at",
            "active_tasks_count",
        ]
        read_only_fields = ["id", "is_active", "created_at", "active_tasks_count"]



class WorkerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ["max_tasks"]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "description",
            "priority",
            "task_type",
        ]
        read_only_fields = ["id"]


class TaskSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "description",
            "priority",
            "status",
            "task_type",
            "created_at",
            "completed_at",
            "worker",
        ]
        read_only_fields = [
            "id",
            "description",
            "priority",
            "task_type",
            "created_at",
            "completed_at",
            "worker",
        ]


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["status"]

    def validate_status(self, value):
        valid_statuses = [s[0] for s in task_status]
        if value not in valid_statuses:
            raise serializers.ValidationError("Invalid status")
        return value

    def update(self, instance: Task, validated_data):
        new_status = validated_data["status"]
        try:
            instance.status = new_status
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        instance.save()
        return instance
