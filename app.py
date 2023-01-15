from flask import Flask

app = Flask(__name__)

import controllers.catalog
import controllers.course
import controllers.register
import controllers.authorize
