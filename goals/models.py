from django.db import models
from django.contrib.auth.models import User
import datetime


def current_year():
    return datetime.datetime.now().year


class ReadingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_goals')
    year = models.PositiveIntegerField(default=current_year)
    target_books = models.PositiveIntegerField(default=12)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'year']
        ordering = ['-year']
    
    def __str__(self):
        return f"{self.user.username}'s {self.year} Reading Goal: {self.target_books} books"
    
    def books_finished(self):
        from books.models import Book
        return Book.objects.filter(
            user=self.user,
            status='finished',
            date_finished__year=self.year
        ).count()
    
    def progress_percentage(self):
        if self.target_books == 0:
            return 0
        return int((self.books_finished() / self.target_books) * 100)
