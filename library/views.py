from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer, CreateTransactionSerializer


# BookViewSet to handle CRUD operations for books
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # Optionally, filter books by availability (only showing books with available copies)
    def get_queryset(self):
        queryset = super().get_queryset()
        available = self.request.query_params.get('available', None)
        if available:
            queryset = queryset.filter(copies_available__gt=0)
        return queryset


# TransactionViewSet to handle book checkouts and returns
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTransactionSerializer
        return TransactionSerializer

    # Endpoint for returning a book
    @action(detail=True, methods=['post'], url_path='return')
    def return_book(self, request, pk=None):
        try:
            transaction = self.get_object()
            if transaction.is_returned:
                return Response({'error': 'Book is already returned'}, status=status.HTTP_400_BAD_REQUEST)
            # Mark the book as returned
            transaction.is_returned = True
            transaction.return_date = timezone.now()
            transaction.book.copies_available += 1
            transaction.book.save()
            transaction.save()
            return Response({'success': 'Book returned successfully'}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
