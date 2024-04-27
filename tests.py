import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
from app import app, db
from app.models import User


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='zeezbaba', email='bossman@gmail.com')
        u.set_password('king')
        self.assertFalse(u.check_password('queen'))
        self.assertTrue(u.check_password('king'))

    def test_avatar(self):
        u = User(username='zeezbaba', email='bossman@gmail.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
