from django.contrib import admin
from .models import Book, Review

# تسجيل موديل Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')

# تسجيل موديل Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'rating', 'created_at')
