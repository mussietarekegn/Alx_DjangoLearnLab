from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass")
        self.other = User.objects.create_user(username="bob", password="pass")
        self.post = Post.objects.create(title="Hello", content="Content", author=self.user)

    def test_list_view(self):
        resp = self.client.get(reverse("blog:post-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Hello")

    def test_detail_view(self):
        resp = self.client.get(reverse("blog:post-detail", kwargs={"pk": self.post.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Content")

    def test_create_requires_login(self):
        resp = self.client.get(reverse("blog:post-create"))
        self.assertNotEqual(resp.status_code, 200)  # redirect to login
        self.client.login(username="alice", password="pass")
        resp = self.client.post(reverse("blog:post-create"), {
            "title": "New",
            "content": "Some",
            "published": True
        })
        self.assertEqual(Post.objects.filter(title="New").count(), 1)

    def test_update_only_author(self):
        url = reverse("blog:post-update", kwargs={"pk": self.post.pk})
        self.client.login(username="bob", password="pass")
        # bob is not author, should not be allowed
        resp = self.client.get(url)
        self.assertNotEqual(resp.status_code, 200)
        # author can access
        self.client.login(username="alice", password="pass")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_delete_only_author(self):
        url = reverse("blog:post-delete", kwargs={"pk": self.post.pk})
        self.client.login(username="bob", password="pass")
        resp = self.client.post(url)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
        self.client.login(username="alice", password="pass")
        resp = self.client.post(url)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
