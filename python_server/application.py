from flask import Flask, render_template, session, request, jsonify
import hashlib
import os
import pdb
import uuid


# EB looks for an 'application' callable by default.
application = Flask(__name__, static_url_path='/static')

application.config.from_object('config')

@application.route('/')
def index(unique_code=None):
    return render_template("index.html")


@application.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 


@application.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host='localhost')
