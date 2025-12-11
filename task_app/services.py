from django.db.models import Count, Q

from task_app.models import Task, Worker


def get_pending_tasks():
    return Task.objects.filter(status="pending", worker__isnull=True).order_by("priority", "created_at")


def get_workers_with_load():
    return Worker.objects.annotate(
        active_tasks_count=Count("tasks", filter=Q(tasks__status__in=["pending", "in_progress"])),
    ).filter(is_active=True)


def adjust_workers(queue_size):
    if queue_size > 10:
        Worker.objects.create(name=f"worker-{Worker.objects.count() + 1}")

    if queue_size < 5:
        workers = Worker.objects.filter(is_active=True).order_by("created_at")
        if workers.count() > 2:
            workers.exclude(id__in=workers[:2]).update(is_active=False)


def assign_pending_tasks():
    tasks = list(get_pending_tasks())
    adjust_workers(len(tasks))
    workers = get_workers_with_load().order_by("active_tasks_count")

    for task in tasks:
        worker = workers.first()
        if worker and worker.active_tasks_count < worker.max_tasks:
            task.worker = worker
            task.save()
            workers = get_workers_with_load().order_by("active_tasks_count")
