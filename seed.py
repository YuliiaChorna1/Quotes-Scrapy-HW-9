import json
import connect
from datetime import datetime

from models import Quotes, Authors, Tag

class DataLoader():
    def __init__(self, filename):
        self.filename = filename

    def load_json(self):
        with open(self.filename, "r", encoding="utf8") as f:
            data = json.load(f)
        return data
    

class DataSeeder:
    def populate_authors(self, authors_data):
        for author in authors_data:
            author_obj = Authors(
                fullname=author['fullname'],
                born_date=datetime.strptime(author['born_date'], '%B %d, %Y'),
                born_location=author['born_location'],
                description=author['description']
            )
            author_obj.save()            

    def populate_quotes(self, quotes_data):
        for quote in quotes_data:
            tags = [Tag(name=tag) for tag in quote['tags']]
            author = Authors.objects(fullname=quote['author']).first()
            try:
                quote_obj = Quotes(
                    tags=tags,
                    author=author.id,
                    quote=quote['quote']
                )
                quote_obj.save()
            except AttributeError:
                print(f"author for this quote not found: \n{quote}")

def main():
    dataseeder = DataSeeder()
    dataseeder.populate_authors(DataLoader('authors.json').load_json())
    dataseeder.populate_quotes(DataLoader('quotes.json').load_json())


if __name__ == '__main__':
    main()