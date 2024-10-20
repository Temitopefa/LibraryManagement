from rest_framework import serializers
from .models import Book, Transaction
from django.contrib.auth.models import User

# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'copies_available']
    
    # Custom validation to ensure ISBN is unique and valid
    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be 13 characters long.")
        return value


# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)  # Nested serializer for the related book
    user = serializers.StringRelatedField(read_only=True)  # Display username instead of full user object

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'checkout_date', 'return_date', 'is_returned']

# Serializer for Creating a Transaction (checking out a book)
class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['book']

    def validate(self, data):
        book = data['book']
        # Check if the book is available for checkout
        if book.copies_available <= 0:
            raise serializers.ValidationError("This book is not available for checkout.")
        return data

    def create(self, validated_data):
        book = validated_data['book']
        # Reduce the number of copies available when a book is checked out
        book.copies_available -= 1
        book.save()
        transaction = Transaction.objects.create(user=self.context['request'].user, **validated_data)
        return transaction
