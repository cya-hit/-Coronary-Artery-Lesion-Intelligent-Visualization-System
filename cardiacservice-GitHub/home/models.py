from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):


class Cardiacdata(db.Model):

    def __repr__(self):
        return 'Cardiacdata:%d'% self.dataid
