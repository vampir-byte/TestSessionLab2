from django.test import TestCase, Client
from StuffTracker.models import Stuff, MyUser


class LoginFail(TestCase):
    def setUp(self):
        self.monkey = Client()
        self.thingList = {"one": ["cat", "dog"], "two": ["cake"]}

        for name, things in self.thingList.items():
            user = MyUser(name=name, password=name)
            user.save()
            for thing in things:
                Stuff(name=thing, owner=user).save()

    def test_emptyPassword(self):
        for name in self.thingList:
            response = self.monkey.post(
                "/", {"name": name, "password": ""}, follow=True
            )
            self.assertEqual(response.context["message"], "bad password")

    def test_anotherUsersPassword(self):
        for name, password in {"one": "two", "two": "one"}.items():
            response = self.monkey.post(
                "/", {"name": name, "password": password}, follow=True
            )
            self.assertEqual(response.context["message"], "bad password")
