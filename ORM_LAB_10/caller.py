import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Book, Author, Review


def find_books_by_genre_and_language(book_genre, book_language):
    books = Book.objects.filter(genre=book_genre, language=book_language)
    return books


def find_authors_nationalities():
    result = []
    authors = Author.objects.filter(nationality__isnull=False)
    for a in authors:
        result.append(f"{a.first_name} {a.last_name} is {a.nationality}")
    return '\n'.join(result)


def order_books_by_year():
    result = []
    books = Book.objects.order_by('publication_year', 'title')
    for b in books:
        result.append(f"{b.publication_year} year: {b.title} by {b.author}")
    return '\n'.join(result)


def delete_review_by_id(review_id):
    reviews_to_delete = Review.objects.get(id=review_id)
    reviews_to_delete.delete()  # можех да го изтрия и горе ама ->
    # нямаше да мога да използвам променливата в принта.
    return f"Review by {reviews_to_delete.reviewer_name} was deleted"


def filter_authors_by_nationalities(searched_nationality):
    authors = (Author.objects
               .filter(nationality=searched_nationality)
               .order_by('first_name', 'last_name')
               )

    # може и така:
    # result = []
    # for a in authors:
    #     result.append(a.biography) if a.biography is not None else result.append(f'{a.first_name} {a.last_name}')
    #  -----------------------------------------------------------------------------------------------------------

    # като долното само ,че го разделих на няколко реда за по - добра четимост
    # result = [a.biography if a.biography is not None else f"{a.first_name} {a.last_name}" for a in authors]
    # -----------------------------------------------------------------------------------------------------------

    result = [a.biography
              if a.biography is not None
              else f"{a.first_name} {a.last_name}"
              for a in authors]

    return '\n'.join(result)


def filter_authors_by_birth_year(first_year, second_year):
    authors = Author.objects.filter(birth_date__year__range=(first_year, second_year)).order_by('-birth_date')
    result = []
    for a in authors:
        result.append(f"{a.birth_date}: {a.first_name} {a.last_name}")

    return '\n'.join(result)


def change_reviewer_name(curr_reviewers_name, new_name):
    Review.objects.filter(reviewer_name=curr_reviewers_name).update(reviewer_name=new_name)
    result = Review.objects.all()
    return result



