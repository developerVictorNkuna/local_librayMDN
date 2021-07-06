from django.shortcuts import render ,reverse
from django.views import generic

# Create your views here.
#import your models/business logic to render it on the browser
from .models import Book,Author,BookInstance,Genre



def index(request):
    """View function for moe page of site"""
    #Generate counts of some of the main objects

    num_books =Book.objects.all().count()
    num_instances=BookInstance.objects.all.count()


    #Available books(status = 'a')

    num_instances_available =BookInstance.objects.filter(
        status_exact='a'
    ).count()

   #    The 'all() is implied by default'
    num_authors =Author.objects.count()
   # 
    context ={
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors}



    #Render the HTML template index.html with data 
    # ...in the context variable
    return reverse(request,'index.html',context=context)




class BookListView(generic.ListView):
    """this class object will search/query our db and
    get all records for the specified model(book)
    then render template located at the specified path"""
    model=Book
    context_object_name ='book_list' 
    #my own name for the lit of books as template variable
    queryset = Book.objects.filter(title__icontains='Swan')[:5]
    template_name='book_list.html'



class BookDetailView(generic.DetailView):
    model = Book

