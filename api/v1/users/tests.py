from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from urllib.parse import urlencode


class UserViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_1 = get_user_model().objects.create(id=1, first_name="Boris", 
                                                     last_name="Simpson", username='one', 
                                                     password="1", is_staff=True)
        cls.user_2 = get_user_model().objects.create(id=2, first_name="Nick", 
                                                     last_name="Simpson", username='two', 
                                                     password="12")
        cls.user_3 = get_user_model().objects.create(id=3, first_name="Nick", 
                                                     last_name="McDonald", username='three', 
                                                     password="123")
        cls.list_url = reverse("api:v1:users-list")
        cls.detail_url = reverse("api:v1:users-detail", kwargs={"pk": cls.user_3.id})

    def setUp(self):
        self.client.force_login(self.user_1)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_create(self):
        data = {
            "username": "four",
            "password": 1234
        }
        response = self.client.post(self.list_url, data=data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            response.json()["id"], 
            get_user_model().objects.values_list("id", flat=True)
        )

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.user_3.id)
        self.assertEqual(response.json()['username'], self.user_3.username)

    def test_update(self):
        data = {
            "username": self.user_3.username,
            "password": self.user_3.password,
            "first_name": "John",
            "last_name": "Smith"
        }

        response = self.client.put(self.detail_url, data=data, format="json")
        self.assertEqual(response.status_code, 200)

        user = get_user_model().objects.filter(id=self.user_3.id).first()
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])

    def test_destroy(self):
        response = self.client.delete(self.detail_url, format="json")
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(
            self.user_3.id, 
            get_user_model().objects.values_list("id", flat=True)
        )

    def test_auth(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)

        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, 403)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)

        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)

    def test_urls(self):
        self.assertEqual(self.list_url, "/api/v1/users")
        self.assertEqual(
            self.detail_url,
            f"/api/v1/users/{self.user_3.id}"
        )

    def test_sort_by(self):
        params = {'sort_by': 'username'}
        response = self.client.get(self.list_url + '?' + urlencode(params))
        self.assertEqual(response.status_code, 200)
        expected_usernames = ['one', 'three', 'two']
        response_usernames = [user["username"] for user in response.json()]
        self.assertEqual(expected_usernames, response_usernames)        

    def test_first_name_filer(self):
        params = {'first_name': 'Boris'}
        response = self.client.get(self.list_url + '?' + urlencode(params))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]["first_name"], params["first_name"])

    def test_last_name_filter(self):
        params = {'last_name': 'McDonald'}
        response = self.client.get(self.list_url + '?' + urlencode(params))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]["last_name"], params["last_name"])
