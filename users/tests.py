from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestUsers(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.login_url = reverse('login')

    def test_success_message_appears(self):
        credentials = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(self.login_url, credentials)
        self.assertRedirects(response, reverse('main'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы залогинены")

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    

