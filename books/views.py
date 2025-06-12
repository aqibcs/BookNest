from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Book, Note
from .forms import BookForm, NoteForm, BookProgressForm


@login_required
def book_list(request):
    books = Book.objects.filter(user=request.user)
    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'books': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'to_read_count': books.filter(status='to_read').count(),
        'reading_count': books.filter(status='reading').count(),
        'finished_count': books.filter(status='finished').count(),
    }
    return render(request, 'books/book_list.html', context)


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    notes = book.notes.all()
    note_form = NoteForm()
    progress_form = BookProgressForm(instance=book)

    context = {
        'book': book,
        'notes': notes,
        'note_form': note_form,
        'progress_form': progress_form,
    }
    return render(request, 'books/book_detail.html', context)


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('book-list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('book-list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})


@login_required
def add_note(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.book = book
            note.save()
            messages.success(request, 'Note added successfully!')
    return redirect('book-detail', pk=book.pk)


@login_required
def delete_note(request, book_pk, note_pk):
    note = get_object_or_404(Note,
                             pk=note_pk,
                             book__pk=book_pk,
                             book__user=request.user)
    note.delete()
    messages.success(request, 'Note deleted successfully!')
    return redirect('book-detail', pk=book_pk)


@login_required
def update_progress(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookProgressForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Progress updated successfully!')
    return redirect('book-detail', pk=book.pk)


@login_required
def filter_books(request, status):
    books = Book.objects.filter(user=request.user, status=status)
    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'books':
        page_obj,
        'status':
        status,
        'is_paginated':
        page_obj.has_other_pages(),
        'page_obj':
        page_obj,
        'to_read_count':
        Book.objects.filter(user=request.user, status='to_read').count(),
        'reading_count':
        Book.objects.filter(user=request.user, status='reading').count(),
        'finished_count':
        Book.objects.filter(user=request.user, status='finished').count(),
    }
    return render(request, 'books/book_list.html', context)


@login_required
def mark_as_finished(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    book.status = 'finished'
    book.save()
    messages.success(request, f'"{book.title}" marked as finished.')
    return redirect('book-list')
