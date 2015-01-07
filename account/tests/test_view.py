# -*- coding: utf-8 -*-

import os
import shutil
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext as _
from django.test import TestCase
from account.models import Staff

from common import factory


class TestLogin(TestCase):
    def setUp(self):
        self.staff = factory.create_staff('crosalot', 'crosalot@gmail.com', 'password')

    def test_anonymous_get_login_page(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_authenticated_get_login_page_will_redirect_to_project_home(self):
        self.client.login(username=self.staff.username, password='password')

        response = self.client.get(reverse('account_login'), follow=True)
        self.assertRedirects(response, reverse('home'))
        self.client.logout()

    def test_login_page_context(self):
        response = self.client.get(reverse('account_login'))
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')

    def test_post_login_with_email(self):
        params = {
            'email': self.staff.email,
            'password': 'password',
        }
        response = self.client.post(reverse('account_login'), params, follow=True)

        self.assertIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse('home'))
        self.client.logout()

    def test_post_login_with_username(self):
        params = {
            'email': self.staff.username,
            'password': 'password',
        }
        response = self.client.post(reverse('account_login'), params, follow=True)

        self.assertIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse('home'))
        self.client.logout()

    def test_post_login_invalid(self):
        # invalid username
        params = {
            'email': '%s.invalid' % self.staff.username,
            'password': 'password',
        }
        response = self.client.post(reverse('account_login'), params)

        self.assertContains(response, _('Please, enter correct email/username and password.'))
        self.assertNotIn('_auth_user_id', self.client.session)

        # invalid password
        params = {
            'email': self.staff.username,
            'password': 'password.invalid',
        }
        response = self.client.post(reverse('account_login'), params)

        self.assertContains(response, _('Please, enter correct email/username and password.'))
        self.assertNotIn('_auth_user_id', self.client.session)

        # invalid active
        self.staff.is_active = False
        self.staff.save()

        params = {
            'email': self.staff.username,
            'password': 'password',
        }
        response = self.client.post(reverse('account_login'), params)

        self.assertContains(response, _('This account not activated.'))
        self.assertNotIn('_auth_user_id', self.client.session)



    def test_logout(self):
        self.client.login(email=self.staff.email, password='password')
        response = self.client.get(reverse('account_logout'))
        self.assertIsNone(self.client.session.get('_auth_user_id'))
        self.assertRedirects(response, reverse('account_login'))
        self.client.logout()


class TestResetPassword(TestCase):

    def setUp(self):
        self.staff = factory.create_staff('crosalot', 'crosalot@gmail.com', 'password')

    def test_anonymous_user_can_access_forget_password_page(self):
        response = self.client.get(reverse('account_reset_password'), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'account/password_reset_form.html')

    def test_authenticated_user_cannot_access_forget_password_page(self):
        self.client.login(username=self.staff.username, password='password')
        response = self.client.get(reverse('account_reset_password'), follow=True)
        self.assertEqual(403, response.status_code)

    def test_forget_password_page_context(self):
        response = self.client.get(reverse('account_reset_password'), follow=True)
        self.assertContains(response, 'name="email"')

    def test_anonymous_user_can_request_password(self):
        params = {
            'email': self.staff.email,
        }
        response = self.client.post(reverse('account_reset_password'), params, follow=True)
        self.assertRedirects(response, reverse('account_reset_password_done'))

        uid = urlsafe_base64_encode(force_bytes(self.staff.id))
        token = default_token_generator.make_token(self.staff)


        self.assertEquals(len(mail.outbox), 1)
        self.assertIn(_('Reset password on'), mail.outbox[0].subject)
        self.assertIn(reverse('account_reset_password_confirm', args=[uid, token, ]), mail.outbox[0].body)


    def test_request_password_with_invalid_email(self):
        params = {
            'email': 'invalid',
        }
        response = self.client.post(reverse('account_reset_password'), params, follow=True)
        self.assertFormError(response, 'form', 'email', [_('Enter a valid email address.')])

    def test_request_password_with_email_that_not_in_system(self):
        params = {
            'email': 'invalid@gmail.com',
        }
        response = self.client.post(reverse('account_reset_password'), params, follow=True)
        self.assertFormError(response, 'form', 'email', [_('Your email address is not registered.')])

    def test_access_reset_password_confirm_form_link_in_email(self):
        uid = urlsafe_base64_encode(force_bytes(self.staff.id))

        token = default_token_generator.make_token(self.staff)
        response = self.client.get(reverse('account_reset_password_confirm', args=[uid, token, ]), follow=True)
        self.assertRedirects(response, reverse('account_edit')+'?reset_password=True')
        self.assertContains(response, _('Please, change your password'))

    def test_invalid_uid_in_reset_password_confirm(self):
        uid = urlsafe_base64_encode(force_bytes(5))
        token = '3ai-e84fa443f006ac46frvp'
        response = self.client.get(reverse('account_reset_password_confirm', args=[uid, token, ]))
        self.assertEqual(404, response.status_code)



class TestEditProfile(TestCase):

    def setUp(self):
        self.staff1 = factory.create_staff('crosalot', 'crosalot@kmail.com', 'password', ' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th')
        self.staff2 = factory.create_staff('panudate', 'panudate@kmail.com', 'password', ' Panudate', 'Vasinwattana', 'Tester', 'Unittest', 'http://opendream.in.th')

    def test_get_edit_profile_page(self):
        response = self.client.get(reverse('account_edit'))
        self.assertRedirects(response, '%s?next=%s' % (reverse('account_login'), reverse('account_edit')))

        self.client.login(username=self.staff1.username, password='password')
        response = self.client.get(reverse('account_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/edit.html')
        self.client.logout()

        self.client.login(username=self.staff2.username, password='password')
        response = self.client.get(reverse('account_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/edit.html')
        self.client.logout()

    def test_edit_profile_context(self):
        self.client.login(username=self.staff1.username, password='password')
        response = self.client.get(reverse('account_edit'))

        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'name="password2"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="occupation"')
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'name="homepage_url"')

        self.assertContains(response, self.staff1.username)
        self.assertContains(response, self.staff1.email)
        self.assertContains(response, self.staff1.first_name)
        self.assertContains(response, self.staff1.last_name)
        self.assertContains(response, self.staff1.occupation)
        self.assertContains(response, self.staff1.description)
        self.assertContains(response, self.staff1.homepage_url)
        self.assertNotContains(response, self.staff1.password)

        self.client.logout()

        self.client.login(username=self.staff2.username, password='password')
        response = self.client.get(reverse('account_edit'))
        self.assertContains(response, self.staff2.username)
        self.assertContains(response, self.staff2.email)
        self.assertContains(response, self.staff2.first_name)
        self.assertContains(response, self.staff2.last_name)
        self.assertContains(response, self.staff2.occupation)
        self.assertContains(response, self.staff2.description)
        self.assertContains(response, self.staff2.homepage_url)
        self.assertNotContains(response, self.staff2.password)

        self.client.logout()

    def test_post_edit_profile_with_password(self):
        params = {
            'username': 'username.change',
            'email': 'email.change@gmail.com',
            'password': '1234',
            'password2': '1234',
            'first_name': 'first name change',
            'last_name': 'last name change',
            'occupation': 'occupation change',
            'description': 'description change',
            'homepage_url': 'http://homepage.url/change',
        }
        self.client.login(username=self.staff1.username, password='password')
        response = self.client.post(reverse('account_edit'), params, follow=True)

        self.assertContains(response, _('Your account profile have been updated.'))
        self.assertEqual(Staff.objects.filter(username=self.staff1.username).count(), 0)
        self.assertEqual(Staff.objects.filter(email=self.staff1.email).count(), 0)

        staff = Staff.objects.get(email="email.change@gmail.com")

        self.assertEqual(staff.first_name, 'first name change')
        self.assertEqual(staff.last_name, 'last name change')
        self.assertEqual(staff.occupation, 'occupation change')
        self.assertEqual(staff.description, 'description change')
        self.assertEqual(staff.homepage_url, 'http://homepage.url/change')

        self.client.logout()

        self.client.login(username=staff.username, password='1234')
        self.assertIn('_auth_user_id', self.client.session)
        self.client.logout()

    def test_post_edit_profile_without_password(self):

        params = {
            'username': 'username.change',
            'email': 'email.change@gmail.com',
            'first_name': 'first name change',
            'last_name': 'last name change',
            'occupation': 'occupation change',
            'description': 'description change',
            'homepage_url': 'http://homepage.url/change',
            'image': 'test.jpg'
        }
        self.client.login(username=self.staff1.username, password='password')

        response = self.client.post(reverse('account_edit'), params, follow=True)

        staff = Staff.objects.get(email="email.change@gmail.com")

        #self.assertEqual(staff.image, 'test.jpg')
        self.assertEqual(staff.first_name, 'first name change')
        self.assertEqual(staff.last_name, 'last name change')
        self.assertEqual(staff.occupation, 'occupation change')
        self.assertEqual(staff.description, 'description change')
        self.assertEqual(staff.homepage_url, 'http://homepage.url/change')
        self.client.logout()

        self.client.login(username=staff.username, password='password')
        self.assertIn('_auth_user_id', self.client.session)
        self.client.logout()

    def test_post_edit_profile_invalid(self):
        self.client.login(username=self.staff1.email, password='password')

        params = {
            'username': '',
            'email': '',
            'first_name': '',
            'last_name': '',
            'occupation': '',
            'description': '',
            'homepage_url': '',
        }
        response = self.client.post(reverse('account_edit'), params)
        self.assertFormError(response, 'form', 'username', [_('This field is required.')])
        self.assertFormError(response, 'form', 'email', [_('This field is required.')])

        params = {
            'password': 'q',
            'password2': 'w',
        }
        response = self.client.post(reverse('account_edit'), params)
        self.assertFormError(response, 'form', 'password2', [_('Password mismatch.')])

        params = {
            'username': self.staff2.username,
            'email': self.staff2.email,
            'first_name': '',
            'last_name': '',
            'occupation': '',
            'description': '',
            'homepage_url': '',
        }
        response = self.client.post(reverse('account_edit'), params)
        self.assertFormError(response, 'form', 'username', [_('This username is already in use.')])
        self.assertFormError(response, 'form', 'email', [_('This email is already in use.')])

        self.client.logout()

    def test_post_edit_profile_not_update(self):
        self.client.login(username=self.staff1.email, password='password')

        params = {
            'username': self.staff1.username,
            'email': self.staff1.email
        }

        response = self.client.post(reverse('account_edit'), params, follow=True)
        self.assertContains(response, _('Your account profile have been updated.'))
