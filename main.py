from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(".env")

# Pulling movie data from The Movie Database using the TMDB API
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

# URL for respective movie's poster
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/original"

year = datetime.now().year

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_CONFIG")
Bootstrap5(app)

# Flask Form used when adding a new movie or editing the review of an existing movie
class EditForm(FlaskForm):
    rating_edit = StringField(label='Your Rating Out of 10', render_kw={"autocomplete":"off"})
    review_edit = StringField(label='Your Review', render_kw={"autocomplete":"off"})
    submit = SubmitField("Done")

# Flask Form used to search TMDB using movie title    
class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()], render_kw={"autocomplete":"off"})
    submit = SubmitField("Add Movie")

class Base(DeclarativeBase):
    pass

# Database used to store movie data
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie_coll.db"
db.init_app(app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

# #with app.app_context():
# #    Movie.query.filter(Movie.id == 3).delete()
# #    db.session.commit()

# Home page showing the watched movies in order of their respective scores (highest to lowest)
@app.route("/", methods=["GET", "POST"])
def home():
    collection = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
    all_movies = collection.scalars().all()
    
    i = 1
    for movie in all_movies:
        movie.ranking = i
        i += 1
    db.session.commit()
    
    return render_template("index.html", movies = all_movies, copyright_year = year)

# Edit page used for altering the score and review of a movie already in database
@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        try:
            movie.rating = float(form.rating_edit.data)
        except ValueError:
            movie.rating = movie.rating
        finally:
            movie.review = form.review_edit.data
            db.session.commit()
        return redirect(url_for('home'))
    
    return render_template("edit.html", movie=movie, form=form, copyright_year = year)

# Function to remove a movie from our database
@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = db.get_or_404(Movie, movie_id)    
    db.session.delete(movie_to_delete)
    db.session.commit()
    
    return redirect(url_for('home'))

auth = os.environ.get("DB_HEADER")

headers = {"accept": "application/json",
            "Authorization": f"Bearer {auth}"
            }

# Search page - loads all movies found on TMDB based on title input
@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"
        response = requests.get(url, params={"query":movie_title}, headers=headers)
        data = response.json()["results"]
        return render_template("select.html", data=data)
    
    return render_template("add.html", form=form, copyright_year = year)

# Function to add the selected movie to the database
@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    
    if movie_api_id:
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        response = requests.get(movie_url, params={"language": "en-US"}, headers=headers)
        data = response.json()
    
        new_movie = Movie(
            title = data["original_title"],
            year = data["release_date"].split("-")[0],
            img_url = f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description = data["overview"]
        )
    
        db.session.add(new_movie)
        db.session.commit()
    
        return redirect(url_for('edit', id=new_movie.id))
        

if __name__ == '__main__':
    app.run(debug=False)
