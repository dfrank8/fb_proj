from flask import Flask, render_template, session, request, jsonify
from flask_assets import Environment, Bundle
import hashlib
import os
import pdb
import uuid


# EB looks for an 'application' callable by default.
application = Flask(__name__, static_url_path='/static')

application.config.from_object('config')

assets = Environment(application)

js_bundle = Bundle(
    'js/copytoclipboard.js',
    'js/script.js',
    filters='jsmin', output='gen/jsmin.js')

css_bundle = Bundle(
    'css/bootstrap.min.css',
    'css/font-awesome.min.css',
    'css/animate.min.css',
    'css/style.css',
    'css/colors/treehoppr.css',
    filters='cssmin', output='gen/cssmin.css')

assets.register('js_all', js_bundle)
assets.register('css_all', css_bundle)

@application.route('/')
def index(unique_code=None):
    return render_template("index.html")

@application.route('/holding')
def holding():
    return render_template("holding.html")

@application.route('/peak')
def peak():
    return render_template("peak.html")


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
