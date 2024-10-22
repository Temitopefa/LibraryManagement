Library Management System API

Project Overview

This is a Django-based Library Management System API that allows users to manage books, borrow and return them, and view their availability. The API leverages Django REST Framework (DRF) for API functionalities and includes basic user authentication using JWT for secure access.

Features
Book Management (CRUD): Allows the creation, reading, updating, and deletion of books.
User Management (CRUD): Enables managing library users with unique usernames and emails.
Book Borrowing and Returning: Users can borrow available books, and return them once done.
Borrowing History: Keeps a log of users' borrowing history, including check-out and return dates.
View Available Books: Displays all available books, with search filters by title, author, and ISBN.

Table of Contents

Installation
Setup
Features and Endpoints
Authentication
Deployment
Technologies Used

Installation

1.Clone the repository:

git clone https://github.com/Temitopefa/LibraryManagement.git
cd library_management_system

2.Install dependencies:
pip install -r requirements.txt

3. Run migrations:
python manage.py migrate

4. Create a superuser for the admin dashboard:
python manage.py createsuperuser

5. Start the development server:
python manage.py runserver

Setup
Books: Books have attributes like Title, Author, ISBN, Published Date, and Copies Available.
Users: Library users have unique usernames, emails, and membership dates.
Transactions: Manages book checkouts and returns by users, logging borrowing history.

Models

Book Model

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1)

Transaction Model

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateField(default=date.today)
    return_date = models.DateField(null=True, blank=True)


Features and Endpoints

Book Management

List all books:
GET /books/
Create a new book:
POST /books/
Retrieve a specific book:
GET /books/{id}/
Update a book:
PUT /books/{id}/
Delete a book:
DELETE /books/{id}/

Transaction Management
Checkout a book:
POST /transactions/
Body: { "book": "book_id" }
Return a book:
POST /transactions/{id}/return/
View borrowing history:
GET /transactions/

Authentication
JWT Login:
POST /api/token/
Body: { "username": "Temi", "password": "Drogba@121" }

JWT Refresh:
POST /api/token/refresh/

Filters and Availability

List available books only:
GET /books/?available=true
Search by title:
GET /books/?title=Book+Title
Search by author:
GET /books/?author=Author+Name
Search by ISBN:
GET /books/?isbn=1234567890123

Authentication
This API uses JWT for authentication. You can log in by obtaining a token using /api/token/ and then use this token in the Authorization header for further API requests.

Example login request:

curl -X POST http://localhost:8000/library/api/token/ 
  -d '{
    "username": "Temi",
    "password": "Drogba@121"
  }'

Once authenticated, include the JWT token in the header:
Authorization: Bearer <token>


Deployment
PythonAnywhere

Technologies Used
Django: Backend framework for building the API.
Django REST Framework: Toolkit for building Web APIs.
JWT: Used for token-based authentication.
SQLite.