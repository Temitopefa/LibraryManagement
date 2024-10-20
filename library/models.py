from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)  # ISBN must be unique
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1)  # Track number of copies available

    def __str__(self):
        return self.title

# Transaction Model (for checkouts and returns)
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to a library user
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateField(default=date.today)
    return_date = models.DateField(null=True, blank=True)  # Can be null until the book is returned

    def __str__(self):
        return f"{self.user.username} checked out {self.book.title}"

    # Check if the book is currently checked out
    @property
    def is_returned(self):
        return self.return_date is not None

