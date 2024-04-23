from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)


@app.route('/')
def index():
    with app.app_context():
        books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/add', methods=['POST'])
def add_book():
    author = request.form.get('author')
    name = request.form.get('name')

    new_book = Book(author=author, name=name)
    with app.app_context():
        db.session.add(new_book)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/clear')
def clear_books():
    with app.app_context():
        Book.query.delete()
        db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Add initial books
        initial_books = [
            {'author': 'George Orwell', 'name': '1984'},
            {'author': 'F. Scott Fitzgerald', 'name': 'The Great Gatsby'},
            {'author': 'Jane Austen', 'name': 'Pride and Prejudice'},
            {'author': 'J.K. Rowling', 'name': 'Harry Potter and the Philosopher\'s Stone'},
            {'author': 'Leo Tolstoy', 'name': 'War and Peace'}
        ]

        for book in initial_books:
            new_book = Book(author=book['author'], name=book['name'])
            db.session.add(new_book)

        db.session.commit()

    app.run(debug=True)


