from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse ,resolve
from .views import *

class HomepageTests(TestCase):

    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_template(self): # new
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/HomePage.html')


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func,home)

    def test_map_url_is_resolved(self):
        url = reverse('map')
        self.assertEqual(resolve(url).func,map)

    def test_search_url_is_resolved(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func,search)

    def test_AbutUs_url_is_resolved(self):
        url = reverse('AbutUs')
        self.assertEqual(resolve(url).func,AbutUs)


