from app import create_app, db
from app.models import Book

app = create_app()
app.app_context().push()

# Sample data
books = [
    {
        "isbn": "9780143127550",
        "title": "The Martian",
        "author": "Andy Weir",
        "length": 384,
        "format": "Paperback"
    },
    {
        "isbn": "9780553418026",
        "title": "Ready Player One",
        "author": "Ernest Cline",
        "length": 384,
        "format": "Hardcover"
    }
]

# Add sample data to the database
for book_data in books:
    book = Book(**book_data)
    db.session.add(book)
db.session.commit()
print("Sample data added successfully.")
