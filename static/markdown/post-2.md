
With Flask-Sqlalchemy's automap_base, I'm able to use tables from an existing database.


    :::python
    Base = automap_base()

    class Accounts(UserMixin,db.Model,Base):
        __tablename__ = `accounts`
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.Integer, unique=True)
        password = db.Column(db.String(100))
        # etc 
        
    Base.prepare(db.engine, reflect=True)


It works well with the Flask-login extension. As long as your class has all the columns of the existing table, it should work.

