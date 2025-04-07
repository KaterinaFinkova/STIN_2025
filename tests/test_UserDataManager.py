import unittest

from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField

from models.UserDataManager import DEFAULT_DATA
from models.forms.UserForm import UserForm
from Application import app


class TestUserDataManager(unittest.TestCase):
    def test_default_values(self):
            with app.test_request_context():
                    form = UserForm()
                    for field in form._fields.values():
                        if type(field) in (StringField, IntegerField):
                            self.assertTrue(field.name in DEFAULT_DATA)

    def test_set_and_get(self):
        with app.app_context():
            app.UserDataManager.set_value("test",8)
            self.assertTrue(8,app.UserDataManager.get_value("test"))