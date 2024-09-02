from django.test import TestCase
from .forms import ShelterRegistrationForm, RegistrationForm, PetRegistrationForm, CatRegistrationForm,EventForm, MeetingForm, ShelterProfileForm, AdopterProfileForm
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from pathlib import Path
from django.urls import reverse

class AdopterFormTest(TestCase): #testing for adopter registration
    def testform(self):
        form_data = {
            'username': 'test',
            'email': 'test@mail.com',
            'password': 'Test@1234',
            'first_name': 'test',
            'last_name': 'test',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def testsameemail(self): #testing duplicate email when creating account

        User.objects.create_user(username='test', email='test@mail.com', password='Test@1234')
        form_data = {
            'username': 'test',
            'email': 'test@mail.com',
            'password': 'Test@1234',
            'first_name': 'test',
            'last_name': 'test',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def testusernamelength(self):   #testing username length error more than 20

        form_data = {
            'username': 'test123456789101112131415',
            'email': 'test@mail.com',
            'password': 'Test@1234',
            'first_name': 'test',
            'last_name': 'test',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class ShelterFormTest(TestCase):

    def testvalid(self):
        form_data = {
            'username': 'shelter',
            'email': 'shelter@mail.com',
            'password': 'Shelter@1234',
            'sheltername': 'shelter',
            'contactnumber': '91234567',
        }
        form = ShelterRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def testusernamelength(self):  
        form_data = {
            'username': 'shelter123456789101112131415',
            'email': 'shelter@mail.com',
            'password': 'Shelter@1234',
            'sheltername': 'shelter',
            'contactnumber': '91234567',
        }
        form = ShelterRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    
    def testvalidcontact(self):  
        form_data = {
            'username': 'shelter',
            'email': 'shelter@mail.com',
            'password': 'Shelter@1234',
            'sheltername': 'shelter',
            'contactnumber': '71123456',
        }
        form = ShelterRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('contactnumber', form.errors)

    def testshelternamelength(self):  
        form_data = {
            'username': 'shelter',
            'email': 'shelter@mail.com',
            'password': 'Shelter@1234',
            'sheltername': 'paws',
            'contactnumber': '71123456',
        }
        form = ShelterRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('sheltername', form.errors)


class PetRegistrationFormTest(TestCase):

    def test_valid(self):
        with open('media/pet_images/persian.jpg', 'rb') as img:
            image = SimpleUploadedFile(name='persian.jpg', content=img.read(), content_type='image/jpeg')

            form_data = {
                'name': 'Sally',
                'breed': 'affenpinscher',
                'age': 5,
                'gender': 'female',
                'size': 'small',
                'color': 'brown',
                'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industrys standard Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industrys standard Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industrys standard',
                'likes': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum is simply dummy text of the printing and typesetting industry. ' ,
                'image': image,
            }
            form = PetRegistrationForm(data=form_data, files={'image': image})
            self.assertTrue(form.is_valid(), form.errors)

class CatRegistrationFormTest(TestCase):

    def test_valid(self):
        with open('media/pet_images/persian.jpg', 'rb') as img:
            image = SimpleUploadedFile(name='persian.jpg', content=img.read(), content_type='image/jpeg')

            form_data = {
                'name': 'Sally',
                'breed': 'persian',
                'age': 5,
                'gender': 'female',
                'size': 'small',
                'color': 'brown',
                'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industrys standard Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industrys standard Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industrys standard',
                'likes': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum is simply dummy text of the printing and typesetting industry. ' ,
                'image': image,
            }
            form = CatRegistrationForm(data=form_data, files={'image': image})
            self.assertTrue(form.is_valid(), form.errors)

class EventFormTest(TestCase):

    def test_event_form_valid(self):
        with open('media/pet_images/persian.jpg', 'rb') as img:
          image = SimpleUploadedFile(name='persian.jpg', content=img.read(), content_type='image/jpeg')
          form_data = {
            'title': 'Charity Event',
            'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industrys standard Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industrys standard Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industrys standard',
            'startdate': "2024-09-30T17:19",
            'enddate': "2024-10-01T19:19",
            'location': 'Abbey Road',
            'image': image, 
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

class MeetingFormTest(TestCase):

    def test_meeting_form_valid(self):
        form_data = {
            'fullname': 'John Doe',
            'phonenumber': '91244367', 
            'address': '123 Main Street, Singapore 123456',
            'email': 'john@mail.com',
            'about': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s.Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s.Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s.',
            'experience': 'yes',
            'meeting_time': "2024-10-01T19:19",
        }
        form = MeetingForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

class ShelterProfileFormTest(TestCase):

    def test_shelter_form_valid(self):
        form_data = {
            'sheltername': 'Dog Shelter',
            'email': 'john@mail.com',
            'contactnumber': '91244568',
        }
        form = ShelterProfileForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

class AdopterProfileFormTest(TestCase):

    def test_adopter_form_valid(self):
        form_data = {
            'adopterFirstName': 'John',
            'adopterLastName': 'Doe',
            'adopteremail': 'john@mail.com',
        }
        form = AdopterProfileForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)