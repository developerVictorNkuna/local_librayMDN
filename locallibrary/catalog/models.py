from django.db import models
from django.urls import reverse #used to generate URLs by reversing the URL pattern
import uuid
# Create your models here.






class BookInstance(models.Model):
    """Model representing a specific copy of a book
    i.e. that can be borrowed from the local library system"""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text="Unique ID for this particular book across  the whole library")
    book=models.ForeignKey('Book', 
        on_delete=models.RESTRICT,
        null=True)
    imprint  =models.CharField(max_length=200)
    due_back=models.DateTimeField(null=True,blank=True)

    LOAN_STATUS=(
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status=models.CharField(
        max_length=1,
        blank=True,
        choices=LOAN_STATUS,
        help_text='Book availability')

    class Meta:
        """this is for odering book table object"""
        ordering =['due_back']




class Genre(models.Model):
    """Model representing a book genre."""
    GENRE=(
        ('Science Fiction'),
        ('Fantasy'),
        ('Finance and Economics'),
        ('Philosophy'),
        ('Law & Politics'),
        ('Children Fairy Tales'),
    )
    
    name=models.CharField(max_length=200,help_text='Enter a book genre (e.g.Science Fition )')
    def __str__(self):
        """String for representing the Model name search our genre and returns its name"""

        return self.name

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book) """
    # GENRE=[
    #     'Science Fiction',
    #     'Fantasy',
    #     'Finance and Economics',
    #     'Philosophy',
    #     'Law & Politics',
    #     'Children Fairy Tales'
    # ]
    title=models.CharField(max_length=200)
    
    #Foreign key used because  Book Model Object/Table can..
    # have one author ,but authors have multiple books
     # Author as a string rather than object because it..
     #  hasn't been declared yet in the file
    author=models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True)
    summary = models.TextField(max_length=1000,help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN',max_length=13,unique=True,help_text="13 Characters <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>")
    """
    #ManyToManyField used because genre can contain many books.
    #Books Model Object can cover many genres.
    #Genre class has already been defined so we can specify the object above
    #  

    """
    genre =models.ManyToManyField(Genre,
        help_text="Select a genre for this book")
    
    def display_genre(self):
        """Create a string for the Genre.
        This is required to display genre in Admin"""
        return ','.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description='Genre'

    
    def __str__(self):
        """
        String for representing the model object.
        """

        return self.title

    def get_absolute_url(self):
        """Returb the url to access a detail record for this book"""
        return reverse("model_detail", kwargs={"pk": self.pk})
    

class Author(models.Model):
    """Model Table SQL object for representing an author """

    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateTimeField(null=True,blank=True)
    date_of_death=models.DateTimeField('Died',null=True,blank=True)


    class Meta:
        ordering=['last_name','first_name']


    def get_absolute_url(self):
        """
        Returns the url to access a particular author table sql instance
        """

        return reverse('author-detail',args=[str(self.id)])


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name},{self.first_name}'
