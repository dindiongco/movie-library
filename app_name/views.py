from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from . import db
from .models import Movie
from .forms import AddMovieForm, UpdateMovieForm, SearchMovieForm
from . import api
from flask_login import login_required, current_user
import requests

bp = Blueprint('views', __name__)


@bp.route('/')
def home():
    response = requests.get(url=api.TOP_RATED_MOVIE, params={
        'api_key': api.API_KEYS,
    })
    data = response.json()['results'][0:9]
    all_movies = Movie.query.order_by(Movie.rating.desc()).limit(3).all()
    db.session.commit()
    return render_template('index.html', movies=all_movies, recommended=data, user=current_user)


@bp.route('/library')
@login_required
def library():
    all_movies = db.session.query(Movie).all()
    return render_template('library.html', movies=all_movies, user=current_user)


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_movie():
    form = SearchMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(url=api.SEARCH_MOVIE_URL, params={
            'api_key': api.API_KEYS,
            'query': movie_title
        })
        data = response.json()['results']
        return render_template('select.html', movies=data)
    return render_template('search.html', form=form)


@bp.route('/add', methods=['GET', 'POST'])
def add_movie():
    movie_id = request.args.get('id')
    movie_url = f'{api.ID_URL}/{movie_id}'
    response = requests.get(url=movie_url, params={
        'api_key': api.API_KEYS,
    })
    data = response.json()
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_to_add = Movie(title=data['original_title'], year=data['release_date'][0:3], description=data['overview'],
                             rating=form.rating.data, review=form.review.data,
                             img_url=f"https://image.tmdb.org/t/p/w500/{data['poster_path']}", user_id=current_user.id)
        db.session.add(movie_to_add)
        db.session.commit()
        return redirect(url_for('views.library'))
    return render_template('add.html', movie=data, form=form)

@bp.route('/edit', methods=['GET', 'POST'])
def edit_movie():
    form = UpdateMovieForm()
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.data.get('rating'))
        movie.review = form.data.get('review')
        db.session.commit()
        return redirect(url_for('views.library'))
    return render_template('edit.html', movie=movie, form=form)

@bp.route('/delete')
def delete_movie():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('views.library'))

@bp.route('/<title>', methods=['GET', 'POST'])
def get_movie_details(title):
    movie_id = request.args.get('id')
    movie_url = f'{api.ID_URL}/{movie_id}'
    response = requests.get(url=movie_url, params={
        'api_key': api.API_KEYS,
    })
    data = response.json()
    return render_template('movie_details.html', movie=data)
