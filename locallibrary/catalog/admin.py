from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display =('last_name','first_name','date_of_birth','date_of_death')
    fields =['first_name','last_name',('date_of_birth','date_of_death')]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title','author','display_genre')
@admin.register(Genre)
class Genre(admin.ModelAdmin):
    pass
@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display=('book','status','borrower','due_back','id')
    list_filter=('status','due_back') 
    fieldsets =(None,{
        'fields':('book','imprint','id')
    }),
    ('Availability',{
        'fields':('status','due_back')
    })   

"""
Tabularinline horizontal layout,
Stackedinline (vertical layout)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
"""

# admin.site.register(Genre)
# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(BookInstance)

