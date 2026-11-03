from django.test import TestCase, Client
from StuffTracker.models import Stuff, MyUser


class LoginFail(TestCase):
    monkey = None
    thingList = None

    def setUp(self):
        # completed
        self.monkey = Client()
        self.thingList = {"one": ["cat", "dog"], "two": ["cake"]}
        # fill test database
        for i in self.thingList.keys():
            temp = MyUser(name=i, password=i)
            temp.save()
            for j in self.thingList[i]:
                Stuff(name=j, owner=temp).save()

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
