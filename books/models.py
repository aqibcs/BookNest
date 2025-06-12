from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Book(models.Model):
    STATUS_CHOICES = (
        ('to_read', 'To Read'),
        ('reading', 'Reading'),
        ('finished', 'Finished'),
    )
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='book_covers', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_read')
    pages = models.PositiveIntegerField(default=0)
    pages_read = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_finished = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    
    class Meta:
        ordering = ['-date_updated']
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})
    
    @property
    def progress(self):
        if self.pages == 0:
            return 0
        return int((self.pages_read / self.pages) * 100)


class Note(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_updated']
    
    def __str__(self):
        return f"Note for {self.book.title} ({self.date_created.strftime('%Y-%m-%d')})"
    