from flask import Flask, request, jsonify

app = Flask(__name__)

# Тестова "база даних" у вигляді списку
books = []

# CREATE
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    books.append(data)
    return jsonify({"message": "Книгу додано"}), 201

# READ
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

# UPDATE
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    if 0 <= book_id < len(books):
        data = request.get_json()
        books[book_id] = data
        return jsonify({"message": "Книгу оновлено"})
    return jsonify({"error": "Книгу не знайдено"}), 404

# DELETE
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    if 0 <= book_id < len(books):
        books.pop(book_id)
        return jsonify({"message": "Книгу видалено"})
    return jsonify({"error": "Книгу не знайдено"}), 404

# Привітання (перевірка сервісу)
@app.route("/")
def hello():
    return "Hello from Python CRUD App on Render!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
