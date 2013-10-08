# -*- coding: utf-8 -*-
"""
    flask.ext.validictory
    ---------------------

    This module provides integration between Flask and Validictory. It lets you validate
    json requests against a schema.

    :copyright: (c) 2013 by innerloop.
    :license: MIT, see LICENSE for more details.
"""
import json

__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = 'Mark Angrish'
__license__ = 'MIT'
__copyright__ = '(c) 2013 by innerloop'
__all__ = ['Validictory']

from functools import wraps

from validictory import validate, SchemaError, FieldValidationError
from werkzeug.exceptions import BadRequest, abort
from flask import current_app, request


class Validictory(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.json_validator = self


def expects_json(schema):
    """
        If you decorate a view with this, it will ensure that the request has been
        submitted as a json before calling the actual view.  If this call fails
        it calls the :attr:`Validictory.validation_error` callback. An example::

            @app.route('/post')
            @expects_json(schema)
            def post():
                ...

        :param func: The view function to decorate.
        :type func: function
    """

    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):

            try:
                request_json = request.get_json()

                if json is None:
                    ValueError('The request MIME type must be \'application/json\'')

                validate(request_json, schema)
            except BadRequest:
                raise ValueError('Json is malformed. Please check your formatting.')
            except SchemaError:
                abort(500, 'Json Schema is malformed')

            return func(*args, **kwargs)

        return decorated_view

    return wrapper