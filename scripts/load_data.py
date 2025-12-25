import csv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Books, Users, Ratings


# Function to load books
def load_books():

    session = SessionLocal()
    books_to_insert = []
    skipped_count = 0

    books_path = Path(__file__).parent.parent / "data" / "raw" / "books.csv"

    with open(books_path, 'r', encoding='utf-8') as file:

        reader = csv.DictReader(file)

        for row in reader:

            book_id = row['book_id']
            title = row['title']
            authors = row['authors']

            if not book_id or not title or not authors:
                skipped_count+=1
                continue

            average_rating = row['average_rating']
            image_url = row['image_url']
            isbn = row['isbn']

            if average_rating:
                average_rating = float(average_rating)
            else:
                average_rating = None

            book = Books(
                book_id = int(book_id),
                title = title,
                authors = authors,
                average_rating = average_rating,
                image_url = image_url,
                isbn = isbn

            )

            books_to_insert.append(book)
        
        session.bulk_save_objects(books_to_insert)
        session.commit()
        print(f'Loaded {len(books_to_insert)} books. Skipped {skipped_count} with missing data')
        session.close()


    

# Function to load ratings
def load_ratings():
    session = SessionLocal()
    ratings_to_insert = []
    unique_users = set()

    ratings_path = Path(__file__).parent.parent / "data" / "raw" / "ratings.csv"

    with open(ratings_path, 'r', encoding='utf-8') as file:

        reader = csv.DictReader(file)

        count = 0
        for row in reader:

            user_id = int(row['user_id'])
            book_id = int(row['book_id'])
            rating_value = int(row['rating'])

            unique_users.add(user_id)

            rating_object = Ratings(
                user_id = user_id,
                book_id = book_id,
                rating = rating_value
            )

            ratings_to_insert.append(rating_object)

            count+=1
            if count >= 100000:
                break
        

        users_to_insert = [Users(user_id=uid) for uid in unique_users]

        session.bulk_save_objects(users_to_insert)
        session.bulk_save_objects(ratings_to_insert)
        session.commit()
        
        print(f'Loaded {len(users_to_insert)} users')
        print(f'Loaded {len(ratings_to_insert)} ratings.')
        session.close()





if __name__ == "__main__":
    load_books()
    load_ratings()
