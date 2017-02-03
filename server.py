"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie
import sqlalchemy



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    #a = jsonify([1, 3])

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("/user_list.html", users=users)


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """show info about user"""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


@app.route('/movies')
def movie_list():
    """Show list of movies"""

    movies = Movie.query.order_by("title asc").all()
    return render_template("/movie_list.html", movies=movies)

# @app.route('/movies/<int:movie_id>')
# def movie_detail(movie_id):
#     """Show ratings for a movie"""

#     movie = Movie.query.get(movie_id)
#     return render_template("movie.html", movie=movie)

@app.route('/register')
def registration_form():
    """Prompts user for username and password"""

    return render_template("/registration_form.html")

@app.route('/register', methods=["POST"])
def log_in():
    """Verifies user within database and logs user in"""

    user = request.form.get("username")
    #password = request.form.get("password")

    try:

        current_user = User.query.filter_by(email=user).one()
        flash('You were successfully logged in')
        session["user_id"] = current_user.user_id

        return render_template('homepage.html')

    except sqlalchemy.orm.exc.NoResultFound:

        return render_template('/registration_form.html')


@app.route('/log_out')
def log_out():
    """Removes a user from a session"""

    del session["user_id"]
    # print session["user_id"]
    flash('You were successfully logged out')
    return render_template('homepage.html')

    #Additional reference for log in/log out can be found in project tracker project

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
