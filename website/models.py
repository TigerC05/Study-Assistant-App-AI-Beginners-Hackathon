from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    
    # Relationship to decks and cue cards
    decks = db.relationship('Deck', backref='user', cascade='all, delete-orphan')
    cue_cards = db.relationship('CueCard', backref='user', cascade='all, delete-orphan')

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=True)  # Self-referential
    
    # Relationship to sub-decks and cue cards
    sub_decks = db.relationship('Deck', backref=db.backref('parent', remote_side=[id]), cascade='all, delete-orphan')
    cue_cards = db.relationship('CueCard', backref='deck', cascade='all, delete-orphan')

    @property
    def sub_decks_recursive(self):
        """
        Recursively retrieves all decks within a deck and its subdecks (and the subdecks of those subdecks, and etc...).
        Returns:
            list: List of Deck objects
        """
        sub_decks = []
        for sub_deck in self.sub_decks:
            sub_decks.append(sub_deck)
            sub_decks.extend(sub_deck.sub_decks_recursive)  # Recursively add sub-decks
        # print("DEBUG: ", self.name, sub_decks)
        return sub_decks
    
    @property
    def cue_cards_recursive(self):
        """
        Recursively retrieves all cue cards from a deck and its sub-decks.
        Returns:
            list: List of CueCard objects.
        """
        cue_cards = self.cue_cards
        for sub_deck in self.sub_decks_recursive:
            cue_cards.extend(sub_deck.cue_cards)
        return cue_cards
    
    

class CueCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front_text = db.Column(db.Text, nullable=False)
    back_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    
    # Spaced Repetition Algorithm fields (SuperMemo 2)
    easiness_factor = db.Column(db.Float, default=2.5)
    repetitions = db.Column(db.Integer, default=0)
    interval = db.Column(db.Integer, default=1)
    days_since_last_review = db.Column(db.Integer, default=0)
    
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
