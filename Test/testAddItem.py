from django.test import TestCase, Client
from StuffTracker.models import Stuff, MyUser

class AddItem(TestCase):
    #need to create database in setup
    monkey=None
    thingList=None

    def setUp(self):
        self.monkey = Client()
        self.thingList = {"one": ["cat", "dog"], "two": ["cake"]}
        self.user = MyUser.objects.create(name="test", password="test")
        self.item = Stuff.objects.create(name="cat", owner=self.user)

    #confirm that after an add item form is submitted, that the new item is in the database and appears in the response webpage
    def testAddItem(self):
        session = self.monkey.session
        session["name"] = self.user.name
        session.save()

        response = self.monkey.post("/things/", {"stuff": "dog"})
        self.assertContains(response, "dog")

    def testAddToDatabase(self):
        session = self.monkey.session
        session["name"] = self.user.name
        session.save()

        self.monkey.post("/things/", {"stuff": "dog"})
        self.assertTrue(Stuff.objects.filter(name="dog", owner=self.user).exists())