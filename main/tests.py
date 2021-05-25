import unittest

from django.test import TestCase
from . import models

class ObjectsTests(unittest.TestCase):

    def test_create_object(self):
        obj = models.ParseModel.objects.create(title="Кровать Азор", url="https://divan.ru")
