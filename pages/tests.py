from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class PageViewTest(TestCase):
    def test_page_detail_status(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Практические курсы по программированию")
        self.assertContains(response, "Привет от Хекслета!")
        self.assertNotContains(response, "Практические курсы по химии")
        self.assertTrue(response.context)

    def test_non_existent_page_returns_404(self):
        response = self.client.get('/page/non-existent-slug/')
        self.assertEqual(response.status_code, 404)

    def test_post_method_not_allowed(self):
        response = self.client.post(reverse('main'))
        self.assertEqual(response.status_code, 405)

    def test_response_content_type(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_context_data(self):
        response = self.client.get(reverse('main'))
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].is_authenticated, False)

    def test_no_unexpected_context_keys(self):
        response = self.client.get(reverse('main'))
        self.assertNotIn('form', response.context)
        self.assertNotIn('title', response.context)

    def test_other_methods_not_allowed(self):
        methods = ['put', 'delete', 'patch', 'head']
        for method in methods:
            func = getattr(self.client, method)
            response = func(reverse('main'))
            self.assertEqual(response.status_code, 405, f"{method.upper()} должен возвращать 405")

    def test_template_errors(self):
        response = self.client.get(reverse('main'))
        self.assertNotContains(response, 'Template error')
    