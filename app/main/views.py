from . import main
from flask import render_template

#main route
@main.route("/")
def index():
    """
    view root page that returns the index page and its data
    """
    return render_template("index.html")