from django import forms
from .models import Book, Note


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'cover_image', 'status', 'pages', 'pages_read', 'date_finished']
        widgets = {
            'date_finished': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        pages = cleaned_data.get('pages')
        pages_read = cleaned_data.get('pages_read')

        if pages_read and pages and pages_read > pages:
            raise forms.ValidationError("Pages read cannot be greater than total pages.")
        return cleaned_data


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class BookProgressForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['pages_read', 'status']