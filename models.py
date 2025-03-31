from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

db = SQLAlchemy()
class heroe ( db.Model ):
    __tablename__ = 'heroes'
    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String( 50 ), nullable=False )
    super_name = db.Column( db.String( 50 ), nullable=False )

    def __repr__( self ):
        return f'<Hero {self.name}>'