import os
import unittest

from flask import Flask, json
from validictory import ValidationError
from flask.ext.validictory import Validictory, expects_json

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['JSONSCHEMA_DIR'] = os.path.join(app.root_path, 'schemas')

validictory = Validictory()
validictory.init_app(app)

test1_schema = {
    'type': 'object',
    'properties':
        {
            'name': {'type': 'string'},
            'address': {'type': 'string'},
            'zip': {'type': 'integer', 'minLength': 5, 'maxLength': 10},
            'country': {'type': 'string', 'minLength': 2, 'maxLength': 2},
            'date-of-birth': {'type': 'string', 'format': 'date'},
            'gender': {'type': 'string', 'required': False, 'enum': ['male', 'female']},
            'email': {'type': 'string', 'format': 'email'},
            'phones':
                {
                    'type': 'object',
                    'properties':
                        {
                            'home': {'required': False, 'type': 'string', 'format': 'phone'},
                            'cell': {'required': False, 'type': 'string', 'format': 'phone'}
                        }
                }
        }
}

test2_schema = {'type': 'object',
                'properties': {'name': {'type': 'string'}, 'email': {'type': 'string', 'format': 'email'}},
                'required': ['email']}


@app.route('/test1', methods=['POST'])
@expects_json(test1_schema)
def test1():
    return 'success'



@app.route('/test2', methods=['POST'])
@expects_json(test2_schema)
def test2():
    return 'success'


@app.errorhandler(ValidationError)
def on_error(e):
    return 'error'


client = app.test_client()


class JsonSchemaTests(unittest.TestCase):
    def test_valid_json(self):
        r = client.post(
            '/test1',
            content_type='application/json',
            data=json.dumps({
                'name': 'Mark Angrish',
                'address': 'Imaginationland',
                'zip': 90210,
                'country': 'AU',
                'date-of-birth': '1999-12-12',
                'gender': 'male',
                'email': 'me@you.com',
                'phones': {'cell': '+1 650-555-1234'}
            })
        )
        self.assertIn('success', r.data)

    def test_invalid_json(self):
        r = client.post(
            '/test2',
            content_type='application/json',
            data=json.dumps({
                'name': 'Britney Spears'
            })
        )
        self.assertIn('error', r.data)