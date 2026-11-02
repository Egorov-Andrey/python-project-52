from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task, Status, Label

# Create your tests here.


class TestModelTask(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author_user', password='pass')
        self.executor = User.objects.create_user(username='executor', password='pass')

        self.status = Status.objects.create(name='New')

        self.label = Label.objects.create(name='Bug')

    def test_task_creation(self):
        task = Task.objects.create(
            name="Task_1",
            description="Testing_task",
            author=self.author,
            status=self.status,
        )
        self.assertEqual(task.name, "Task_1")
        self.assertIsNotNone(task.created_at)

    def test_unique_name_constraint(self):
        Task.objects.create(name="Unique Task", status=self.status)

        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Task.objects.create(name="Unique Task", status=self.status, author=self.author)

    def test_many_to_many_labels(self):
        task = Task.objects.create(name="Labeled Task", status=self.status, author=self.author)
        task.labels.add(self.label)

        self.assertIn(self.label, task.labels.all())
        self.assertEqual(task.labels.count(), 1)

