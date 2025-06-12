from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book-list'),
    path('<int:pk>/', views.book_detail, name='book-detail'),
    path('new/', views.book_create, name='book-create'),
    path('<int:pk>/update/', views.book_update, name='book-update'),
    path('<int:pk>/delete/', views.book_delete, name='book-delete'),
    path('<int:pk>/add-note/', views.add_note, name='add-note'),
    path('<int:book_pk>/delete-note/<int:note_pk>/', views.delete_note, name='delete-note'),
    path('<int:pk>/update-progress/', views.update_progress, name='update-progress'),
    path('filter/<str:status>/', views.filter_books, name='filter-books'),
    path('<int:pk>/finish/', views.mark_as_finished, name='book-finish'),
]
