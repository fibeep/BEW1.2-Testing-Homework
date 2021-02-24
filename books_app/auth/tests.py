import os

from unittest import TestCase

from datetime import date

from books_app import app, db, bcrypt
from books_app.models import Book, Author, User, Audience

"""
Run these tests with the command:
python -m unittest books_app.main.tests
"""

#################################################
# Setup
#################################################

def create_books():
    a1 = Author(name='Harper Lee')
    b1 = Book(
        title='To Kill a Mockingbird',
        publish_date=date(1960, 7, 11),
        author=a1
    )
    db.session.add(b1)

    a2 = Author(name='Sylvia Plath')
    b2 = Book(title='The Bell Jar', author=a2)
    db.session.add(b2)
    db.session.commit()


def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

    

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        # : Write a test for the signup route. It should:
        # - Make a POST request to /signup, sending a username & password
        # - Check that the user now exists in the database
        post_data = {
            'username': 'Test User',
            'password' : '12345'
        }
        self.app.post('/signup', data=post_data)
        
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Test User', response_text)

    def test_signup_existing_user(self):
        # : Write a test for the signup route. It should:
        # - Create a user
        # create_user()
        # # - Make a POST request to /signup, sending the same username & password
        # post_data = {
        #     'username': 'Test User',
        #     'password': '12345'
        # }
        # self.app.post('/signup', data=post_data)
        
        # # - Check that the form is displayed again with an error message
        # response = self.app.get('/signup', follow_redirects=True)
        # response_text = response.get_data(as_text=True)
        # self.assertIn('Error', response_text)
        pass
        

    def test_login_correct_password(self):
        # : Write a test for the login route. It should:
        # - Create a user
        # create_user()
        # # - Make a POST request to /login, sending the created username & password
        # post_data = {
        #     'username': 'me1',
        #     'password': 'password_hash'
        # }
        # self.app.post('/login', data=post_data)
        # # - Check that the user's name is now displayed on the homepage
        # response = self.app.get('/login', follow_redirects=True)
        # response_text = response.get_data(as_text=True)
        # self.assertIn('Test User', response_text)
        pass
        

    def test_login_nonexistent_user(self):
        # : Write a test for the login route. It should:
        # - Make a POST request to /login, sending a username & password
        # post_data = {
        #     'username': 'Test User',
        #     'password': '12345'
        # }
        # self.app.post('/login', data=post_data)
        # # - Check that the login form is displayed again, with an appropriate
        # response = self.app.get('/login', follow_redirects=True)
        # response_text = response.get_data(as_text=True)
        # #   error message
        # self.assertIn('Error', response_text)
        pass
        

    def test_login_incorrect_password(self):
        # TODO: Write a test for the login route. It should:
        # - Create a user
        create_user()
        # - Make a POST request to /login, sending the created username &
        #   an incorrect password
        # - Check that the login form is displayed again, with an appropriate
        #   error message
        pass

    def test_logout(self):
        # : Write a test for the logout route. It should:
        # - Create a user
        create_user()
        # - Log the user in (make a POST request to /login)
        post_data = {
            'username': 'Test User',
            'password': '12345'
        }
        self.app.post('/login', data=post_data)
        # - Make a GET request to /logout
        response = self.app.get('/logout', follow_redirects=True)
        # - Check that the user's name does not appear on the homepage
        response_text = response.get_data(as_text=True)
        self.assertNotIn('me1', response_text)
        
