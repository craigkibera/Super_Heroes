from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)
    
    hero_powers = db.relationship('HeroPower',back_populates='hero',cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Hero {self.name}>'

class Power(db.Model):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(20), nullable=False)
    hero_powers = db.relationship('HeroPower',back_populates='power',cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Power {self.name}>'

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(10), nullable=False)  
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id', ondelete="CASCADE"), nullable=False)  # Fixed typo
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id', ondelete="CASCADE"), nullable=False)
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def validates_strength(self, key, value):
        allowed = ["Strong", "Weak", "Average"]  
        if value not in allowed:
            raise ValueError(f"Invalid strength: {value}. Must be one of {allowed}")
        return value
    
    def __repr__(self):
        return f'<Hero Power {self.hero_id} - {self.power_id}>'
