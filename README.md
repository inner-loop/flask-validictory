flask-validictory
=================

Simple integration between Flask and Validictory.

Usage
-----

The easiest way to get everything working is as follows:

    # Note that this is a python dict rather than pure json. This allows
    # you to aggregate common aspects of schemas.
    test1_schema = {'type': 'object',
                    'properties': {'name': {'type': 'string'}, 'email': {'type': 'string', 'format': 'email'}},
                    'required': ['email']}

    @app.route('/test1', methods=['POST'])
    @expects_json(test1_schema)
    def test1():
        json = response.json()
        # do some work
        
    @app.errorhandler(FieldValidationError)
    def on_error(e):
        return 'error'
        
You can also set up an error handler for ValueError to handle poorly formed Json.
