from flask import Flask, render_template, session, request, jsonify
import os
import pdb
import uuid
from flask_compress import Compress
from flask_assets import Environment, Bundle

# EB looks for an 'application' callable by default.
application = Flask(__name__, static_url_path='/static')