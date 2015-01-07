from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db import IntegrityError, transaction

from common import factory

class TestStaff(TestCase):

    def test_create_staff(self):


        staff1 = factory.create_staff('crosalot', 'crosalot@kmail.com', 'password', ' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th')
        self.assertEqual(staff1.first_name, ' Crosalot')
        self.assertEqual(staff1.last_name, 'Opendream ')
        self.assertEqual(staff1.username, 'crosalot')
        self.assertEqual(staff1.email, 'crosalot@kmail.com')
        self.assertEqual(staff1.occupation, 'Developer')
        self.assertEqual(staff1.description, 'Opensource')
        self.assertEqual(staff1.homepage_url, 'http://opendream.co.th')
        self.assertEqual(staff1.get_full_name(), 'Crosalot Opendream')
        self.assertEqual(staff1.get_short_name(), 'Crosalot.O')
        #self.assertEqual(staff1.image, 'test.jpg')

        staff2 = factory.create_staff('panudate', 'panudate@kmail.com', 'password', ' Panudate', 'Vasinwattana', 'Tester', 'Unittest', 'http://opendream.in.th')
        self.assertEqual(staff2.first_name, ' Panudate')
        self.assertEqual(staff2.last_name, 'Vasinwattana')
        self.assertEqual(staff2.username, 'panudate')
        self.assertEqual(staff2.email, 'panudate@kmail.com')
        self.assertEqual(staff2.occupation, 'Tester')
        self.assertEqual(staff2.description, 'Unittest')
        self.assertEqual(staff2.homepage_url, 'http://opendream.in.th')
        self.assertEqual(staff2.get_full_name(), 'Panudate Vasinwattana')
        self.assertEqual(staff2.get_short_name(), 'Panudate.V')
        #self.assertEqual(staff1.image, 'test.jpg')

        staff3 = get_user_model().objects.create(username='staff3', email='staff3@tester.com', password='password', first_name=' Panudate ', last_name='')
        self.assertEqual(staff3.get_full_name(), 'Panudate')
        self.assertEqual(staff3.get_short_name(), 'Panudate')

        staff4 = get_user_model().objects.create(username='staff4', email='staff4@tester.com', password='password', first_name='', last_name=' Vasinwattana ')
        self.assertEqual(staff4.get_full_name(), 'Vasinwattana')
        self.assertEqual(staff4.get_short_name(), 'Vasinwattana')



        try:
            with transaction.atomic():
                factory.create_staff('crosalot')

            self.assertTrue(0, 'Duplicate username allowed.')

        except IntegrityError:
            pass


        try:
            with transaction.atomic():
                factory.create_staff(email='crosalot@kmail.com')

            self.assertTrue(0, 'Duplicate username allowed.')

        except IntegrityError:
            pass