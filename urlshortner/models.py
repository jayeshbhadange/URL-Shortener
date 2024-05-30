from .extensions import db
import string
from random import choices
class URL(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    orignal_url=db.Column(db.String(500),nullable=False)
    short_url=db.Column(db.String(5),nullable=False,unique=True)   
    clicks=db.Column(db.Integer,default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()
    def generate_short_link(self):
        characters=string.digits+string.ascii_letters
        short_url=''.join(choices(characters,k=5))
        #check if short url already exists
        link = self.query.filter_by(short_url=short_url).first()
        if link:
            return self.generate_short_link()
        return short_url