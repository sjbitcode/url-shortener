from django.test import TestCase
from django.core.urlresolvers import reverse

from users.models import User
from .forms import LinkForm
from .models import Link


class LinkTests(TestCase):
    fixtures = ['users', 'links']

    def test_link_form(self):

        # Create VALID short url.
        #
        form = LinkForm({
            'destination': 'http://example1.com'
        })

        # Ensure that the link form is valid.
        self.assertEqual(form.is_valid(), True)

        link = form.save()

        # Ensure that the link has no associated User.
        self.assertEqual(link.user, None)

        # Create INVALID short url.
        #
        invalid_key = link.key
        form = LinkForm({
            'destination': 'http://website1.com',
            'key': invalid_key
        })

        # Ensure that the link form is invalid. In this case, the key
        # should already exist in the database and therefore raise an error.
        self.assertEqual(form.is_valid(), False)

    def test_link_form_user(self):

        user = User.objects.first()

        # Create VALID short url.
        #
        form = LinkForm({
            'destination': 'http://example2.com'
        }, user=user)

        # Ensure that the Link form is valid.
        self.assertEqual(form.is_valid(), True)

        link = form.save()

        # Ensure that the Link has an associated User.
        self.assertEqual(link.user, user)

    def test_guest_link_post(self):
        '''
        Test the 'shorten-url' endpoint with VALID
        data from a guest User.
        '''

        url = reverse('shorten-url')

        # Prepare data and POST it.
        data = {'destination': 'http://website2.com'}
        response = self.client.post(url, data=data)

        # Check the response status code and response data.
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response_data)

        link = Link.objects.get(key=response_data.get('url'))
        # Check that the Link has no associated User.
        self.assertEqual(link.user, None)

    def test_user_link_post(self):
        '''
        Test the 'shorten-url' endpoint with VALID
        data from a logged in User.
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        url = reverse('shorten-url')

        # Prepare data and POST it.
        data = {'destination': 'http://website3.com'}
        response = self.client.post(url, data=data)

        # Check the response status code and response data.
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response_data)

        link = Link.objects.get(key=response_data.get('url'))
        # Check that the Link has an associated User.
        self.assertEqual(link.user, user)
