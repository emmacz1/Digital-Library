from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app import db
from app.models import Book
from app.auth import auth

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@bp.route('/books/<int:id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return render_template('book.html', book=book)

@bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        data = request.form
        book = Book(
            isbn=data['isbn'],
            title=data['title'],
            author=data['author'],
            length=data['length'],
            format=data['format']
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('add_book.html')

@bp.route('/update_book/<int:id>', methods=['GET', 'POST'])
@auth.login_required
def update_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        book.isbn = data['isbn']
        book.title = data['title']
        book.author = data['author']
        book.length = data['length']
        book.format = data['format']
        db.session.commit()
        return redirect(url_for('routes.get_book', id=book.id))
    return render_template('update_book.html', book=book)

@bp.route('/delete_book/<int:id>', methods=['POST'])
@auth.login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('routes.index'))
