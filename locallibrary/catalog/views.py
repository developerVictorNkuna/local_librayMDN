from django.shortcuts import render ,get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from datetime import date
from django.views import  generic

# Create your views here.
#import your models/business logic to render it on the browser
from .models import Book,Author,BookInstance,Genre
import datetime
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

from catalog.forms import  RenewBookForm


@login_required
@permission_required('catalog.can_mark_returned',raise_exception=True)
def renew_book_librarian(request,pk):
    """
    View function for renewing a specific BookInstance..
    by librarian (Users from Admin)

    """
    book_instance=get_object_or_404(BookInstance, pk=pk)

    #if this is a POST method request then  process the form data
    if request.method =='POST':
        form=RenewBookForm(request.POST)

        #check if the form is valid
        if form.is_valid():
            book_instance.due_back=form.cleaned_date['renewal_date']
            book_instance.save()

            #redirect  to a new URL
            return HttpResponseRedirect(reverse('all-borrowed'))
    #if this is a GET (or any other method ) create a default form
    else:
        proposed_renewal_date=datetime.date.today()+datetime.timedelta(weeks=3)
        form =RenewBookForm(initial={"renewal_date":proposed_renewal_date})

        context ={
            "form":form,
            "book_instance":book_instance
        }



        return render(request,'book_renew_librarian.html',context)







class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_visits =request.session.get('num_visits',0)
    request.session['num_visits']=num_visits +1

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits':num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    """this class object will search/query our db and
    get all records for the specified model(book)
    then render template located at the specified path"""
    model=Book
    paginate_by=5

    # context_object_name ='book_list' 
    #my own name for the lit of books as template variable
    # queryset = Book.objects.filter(title__icontains='Swan')[:5]
    #fetch the fist five data items,books that contains 'Swan' of the data object 
    template_name='book_list.html'



class BookDetailView(generic.DetailView):
    model = Book
    paginate_by=5
    template_name='book_detail.html'

