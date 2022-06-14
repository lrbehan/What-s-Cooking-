from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

API_KEY = os.environ['SPOONACULAR_KEY']

@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')