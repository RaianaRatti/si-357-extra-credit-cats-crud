from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Breed, Cat


class CatsCrudTests(TestCase):
    def setUp(self):
        User.objects.create_user("dj4e_user", password="test_password_123")

    def test_login_required(self):
        resp = self.client.get(reverse("cats:all"))
        self.assertRedirects(resp, "/accounts/login/?next=/cats/")

    def test_meta_tag_on_pages(self):
        self.client.login(username="dj4e_user", password="test_password_123")
        for url in ["/", "/accounts/login/", reverse("cats:all"), reverse("cats:breed_list"),
                    reverse("cats:breed_create"), reverse("cats:cat_create")]:
            self.assertContains(self.client.get(url), 'name="dj4e" content="05dfff5cf7a5d8bde1ee6e8951cc382b"')

    def test_hand_test_flow(self):
        # Log in through the real login form
        resp = self.client.post(reverse("login"), {
            "username": "dj4e_user", "password": "test_password_123", "next": "/cats/"})
        self.assertRedirects(resp, "/cats/")
        self.assertContains(self.client.get("/cats/"), "Please add a breed before you add a cat.")

        # Add, view, and update a breed
        resp = self.client.post(reverse("cats:breed_create"), {"name": "Tabby"})
        self.assertRedirects(resp, "/cats/")
        breed = Breed.objects.get(name="Tabby")
        self.assertContains(self.client.get(reverse("cats:breed_list")), "Tabby")
        self.client.post(reverse("cats:breed_update", args=[breed.id]), {"name": "Persian"})
        self.assertContains(self.client.get(reverse("cats:breed_list")), "Persian")

        # Add, view, update, and delete a cat
        resp = self.client.post(reverse("cats:cat_create"), {
            "nickname": "Whiskers", "weight": 9, "foods": "tuna", "breed": breed.id})
        self.assertRedirects(resp, "/cats/")
        cat = Cat.objects.get(nickname="Whiskers")
        resp = self.client.get("/cats/")
        self.assertContains(resp, "Whiskers")
        self.assertContains(resp, "Add a cat")
        self.client.post(reverse("cats:cat_update", args=[cat.id]), {
            "nickname": "Mittens", "weight": 10, "foods": "salmon", "breed": breed.id})
        self.assertContains(self.client.get("/cats/"), "Mittens")
        self.assertContains(self.client.get(reverse("cats:cat_delete", args=[cat.id])), "Mittens")
        self.client.post(reverse("cats:cat_delete", args=[cat.id]))
        self.assertFalse(Cat.objects.exists())

        # Delete the breed
        self.client.post(reverse("cats:breed_delete", args=[breed.id]))
        self.assertContains(self.client.get(reverse("cats:breed_list")), "There are no breeds")

    def test_validation_errors(self):
        self.client.login(username="dj4e_user", password="test_password_123")
        resp = self.client.post(reverse("cats:breed_create"), {"name": "X"})
        self.assertContains(resp, "Breed must be greater than 1 character")
        self.assertFalse(Breed.objects.exists())

    def test_logout(self):
        self.client.login(username="dj4e_user", password="test_password_123")
        self.client.post(reverse("logout"))
        self.assertEqual(self.client.get("/cats/").status_code, 302)
