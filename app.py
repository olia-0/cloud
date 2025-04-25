# from flask import Flask, request, jsonify
#
# app = Flask(__name__)
#
# # Тестова "база даних" у вигляді списку
# books = []
#
# # CREATE
# @app.route("/books", methods=["POST"])
# def add_book():
#     data = request.get_json()
#     books.append(data)
#     return jsonify({"message": "Книгу додано"}), 201
#
# # READ
# @app.route("/books", methods=["GET"])
# def get_books():
#     return jsonify(books)
#
# # UPDATE
# @app.route("/books/<int:book_id>", methods=["PUT"])
# def update_book(book_id):
#     if 0 <= book_id < len(books):
#         data = request.get_json()
#         books[book_id] = data
#         return jsonify({"message": "Книгу оновлено"})
#     return jsonify({"error": "Книгу не знайдено"}), 404
#
# # DELETE
# @app.route("/books/<int:book_id>", methods=["DELETE"])
# def delete_book(book_id):
#     if 0 <= book_id < len(books):
#         books.pop(book_id)
#         return jsonify({"message": "Книгу видалено"})
#     return jsonify({"error": "Книгу не знайдено"}), 404
#
# # Привітання (перевірка сервісу)
# @app.route("/")
# def hello():
#     return "Hello from Python CRUD App on Render! -------"
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Підключення до бази даних через змінну середовища
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель книги
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "author": self.author, "year": self.year}

# Створення таблиці при першому запуску
with app.app_context():
    db.create_all()

# Стартова сторінка
@app.route("/")
def hello():
    return "Hello from Python CRUD App with PostgreSQL!"

# CREATE
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], year=data.get('year'))
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Книгу додано", "book": new_book.to_dict()}), 201

# READ
@app.route("/books", methods=["GET"])
def get_books():
    all_books = Book.query.all()
    return jsonify([book.to_dict() for book in all_books])

# UPDATE
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book:
        data = request.get_json()
        book.title = data['title']
        book.author = data['author']
        book.year = data.get('year')
        db.session.commit()
        return jsonify({"message": "Книгу оновлено", "book": book.to_dict()})
    return jsonify({"error": "Книгу не знайдено"}), 404

# DELETE
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Книгу видалено"})
    return jsonify({"error": "Книгу не знайдено"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
