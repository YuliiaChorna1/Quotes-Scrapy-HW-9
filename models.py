from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import DateField, EmbeddedDocumentField, ListField, StringField, ReferenceField


class Tag(EmbeddedDocument):
    name = StringField()

class Authors(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()

class Quotes(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Authors, reverse_delete_rule=2)
    quote = StringField()
