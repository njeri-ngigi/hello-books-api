'''test_api.py'''
import unittest
import json
from api import app

class TestApiEndpoints(unittest.TestCase):
    '''class to tests app.py'''
    def setUp(self):
        '''create a test client'''
        with app.APP.app_context():
            self.client = app.APP.test_client
    def test_api_can_add_book(self):
        '''test that API can add a book (POST request)'''
        response = self.client().post('/api/v1/books', data=json.dumps(
            {"book_id":16, "title": "Queer cats, An African Tale",
             "author":"Chimamano Nakote"}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_api_can_get_all_books(self):
        '''test that api can get all books (GET request)'''
        response = self.client().get('/api/v1/books')
        self.assertEqual(response.status_code, 200)

    def test_api_can_get_book_by_id(self):
        '''test that api can retrieve book by id (GET request)'''
        response = self.client().get('/api/v1/books/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Fly away birdie", str(response.data))
    def test_book_can_be_edited(self):
        '''test that api can modify book'''
        res = self.client().put('/api/v1/books/2',
                                data=json.dumps({"title":"The fault in our stars", 
                                                 "author":"John Greene",
                                                 "edition": "7th"}), 
                                content_type='application/json')
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/api/v1/books/2')
        self.assertIn("John Greene", str(results.data))

    def test_delete_book(self):
        '''test that api can delete book (POST request)'''
        res = self.client().post('/api/v1/books', content_type='application/json',
                                 data=json.dumps({"book_id":16,
                                                  "title": "Queer cats, An African Tale",
                                                  "author": "Chimamano Nakote"}))
        self.assertEqual(res.status_code, 200)
        res = self.client().delete('/api/v1/books/16')
        self.assertEqual(res.status_code, 200)
        #test to check whether deleted item exists
        result = self.client().get('/api/v1/books/16')
        self.assertIn("Book not found", result.data)

    def test_user_actions(self):
        '''method to test register, login, borrow book, logout and reset_password endpoints'''
        result = self.client().post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"username":"hawa", "name":"Hawaii Yusuf",
                                                     "email":"hawa@gma.com", "password":"where",
                                                     "confirm_password":"where"}))
        self.assertEqual(result.status_code, 200)

        result2 = self.client().post('/api/v1/auth/login', content_type='application/json',
                                     data=json.dumps({"username":"hawa", "password":"where"}))
        a_token = result2.data
        self.assertEqual(result2.status_code, 200)

        result3 = self.client().post('/api/v1/users/books/2',
                                     headers=dict(Authorization="Bearer "+ a_token))
        self.assertEqual(result3.status_code, 200)

        result4 = self.client().post('/api/v1/auth/logout',
                                     headers=dict(Authorization="Bearer " + a_token))
        self.assertIn('Successfully logged out', result4.data)

        result5 = self.client().post('/api/v1/auth/reset-password', content_type='application/json',
                                     data=json.dumps({"username":"hawa"}))
        self.assertEqual(result5.status_code, 200)


    def test_reset_password(self):
        '''test reset password method = "POST"'''
        result = self.client().post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"username": "lucy", "name": "Morningstar",
                                                     "email": "lucy@hot.com", "password": "1234",
                                                     "confirm_password": "1234"}))
        self.assertEqual(result.status_code, 200)

        result = self.client().post('/api/v1/auth/reset-password', content_type="application/json",
                                    data=json.dumps({"username":"lucy"}))
        self.assertEqual(result.status_code, 200)
if __name__ == "__main__":
    unittest.main()
