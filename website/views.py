from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import *
from . import db
import json
from .html_logic import display_deck_heirarchy_html, display_deck_list_html


views = Blueprint('views', __name__)

# ------- PAGES -------

@views.route('/') # This is a route decorator, it tells Flask what URL should trigger the function
def home():
    
    return render_template("home.html", user=current_user)

@views.route('/decks', methods=['GET', 'POST'])
@login_required # This is a decorator from Flask-Login that requires the user to be logged in
def decks():

    if request.method == 'POST':
        deck_name = request.form.get('deck_name')
        parent_deck_id = request.form.get('parent_deck')
        if not deck_name:
            flash("Deck name cannot be empty.", category='error')
        else:
            new_deck = Deck(name=deck_name, user_id=current_user.id)

            if parent_deck_id:
                parent_deck = Deck.query.get(parent_deck_id)
                if parent_deck and parent_deck.user_id == current_user.id:
                    new_deck.parent_id = parent_deck.id
            
            db.session.add(new_deck)
            db.session.commit()
            
            flash(f'Deck "{deck_name}" created successfully!', "success")

    user_decks = Deck.query.filter_by(user_id=current_user.id).all()


    return render_template("decks.html", user=current_user, decks=user_decks, display_deck_heirarchy_html=display_deck_heirarchy_html, display_deck_list_html=display_deck_list_html)

@views.route('/decks/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def overview_deck(deck_id):
    deck = Deck.query.get(deck_id)
    if deck is None or deck.user_id != current_user.id:
        flash("Deck not found or you don't have permission to view it.", category='error')
        return redirect('/decks')
    
    if request.method == 'POST':
        # Delete the deck (a POST request will only run if the user clicks the delete button)
        # TODO: Implement the logic to delete the deck or warn about deleting a deck with sub-decks
        return redirect('/decks')

    cue_cards = deck.cue_cards_recursive

    return render_template("overview-deck.html", user=current_user, deck=deck, cue_cards=cue_cards)

@views.route('/decks/<int:deck_id>/add-cards', methods=['GET', 'POST'])
@login_required
def add_cards(deck_id):
    deck = Deck.query.get(deck_id)
    if deck is None or deck.user_id != current_user.id:
        flash("Deck not found or you don't have permission to view it.", category='error')
        return redirect('/decks')
    
    # TODO: Implement the logic to add cards to the deck
    if request.method == 'POST':
        front_text = request.form.get('front_text')
        back_text = request.form.get('back_text')

        if not front_text or not back_text:
            flash("Both front and back text are required.", category='error')
        else:
            new_card = CueCard(front_text=front_text, back_text=back_text, deck_id=deck.id, user_id=current_user.id)
            db.session.add(new_card)
            db.session.commit()
            flash("Card added successfully!", category='success')

    cue_cards = deck.cue_cards_recursive

    return render_template("add-cards.html", user=current_user, deck=deck, cue_cards=cue_cards)

@views.route('/decks/<int:deck_id>/study', methods=['GET'])
@login_required
def study_deck(deck_id):
    deck = Deck.query.get(deck_id)
    if deck is None or deck.user_id != current_user.id:
        flash("Deck not found or you don't have permission to view it.", category='error')
        return redirect('/decks')
    
    # TODO: Implement the logic to study the deck

    return render_template("study-deck.html", user=current_user, deck=deck)

@views.route('/decks/<int:deck_id>/browse', methods=['GET'])
@login_required
def browse_deck(deck_id):
    deck = Deck.query.get(deck_id)
    if deck is None or deck.user_id != current_user.id:
        flash("Deck not found or you don't have permission to view it.", category='error')
        return redirect('/decks')
    cue_cards = deck.cue_cards_recursive
    # for cue_card in cue_cards:
    #     print(cue_card.deck_id)
    return render_template("browse-deck.html", user=current_user, deck=deck, cue_cards=cue_cards)

@views.route('/delete-card', methods=['POST'])
@login_required
def delete_card():
    card_id = request.form.get('card_id')

    if card_id:
        card = CueCard.query.filter_by(id=card_id, user_id=current_user.id).first()
        if card:
            db.session.delete(card)
            db.session.commit()
            flash(f'Card "{card.front_text}" deleted successfully!', "success")
        else:
            flash("Card not found or unauthorized.", "error")
    else:
        flash("Invalid request.", "error")

    return redirect(url_for('views.browse_deck', deck_id=card.deck_id))


@views.route('/delete-deck/<int:deck_id>', methods=['POST'])
@login_required
def delete_deck_and_cards(deck_id):
    """
    Delete a deck and all its sub-decks and cards.
    WARNING: This will delete all cards in the deck and its sub-decks.
    """
    deck = Deck.query.get(deck_id)
    if deck is None or deck.user_id != current_user.id:
        flash("Deck not found or you don't have permission to delete it.", category='error')
        return redirect(url_for('views.decks'))
    
    # Delete all cards in the deck and its sub-decks
    for card in deck.cue_cards_recursive:
        db.session.delete(card)
    
    # Delete all sub-decks
    for sub_deck in deck.sub_decks_recursive:
        db.session.delete(sub_deck)
    
    # Delete the deck itself
    db.session.delete(deck)
    db.session.commit()
    flash(f'Deck "{deck.name}" and all its sub-decks and cards deleted successfully!', "success")

    return redirect(url_for('views.decks'))

@views.route('/delete-deck-displace-subs/<int:deck_id>', methods=['POST'])
@login_required
def delete_deck_but_displace_sub_decks(deck_id):
    """
    Delete a deck but displace its sub-decks to the parent deck.
    WARNING: This will delete all cards directly stored in the deck.
    """
    deck = Deck.query.get(deck_id)
    if deck is None or deck.user_id != current_user.id:
        flash("Deck not found or you don't have permission to delete it.", category='error')
        return redirect(url_for('views.decks'))
    
    # Move all sub-decks to the parent deck
    parent_deck = deck.parent
    sub_decks = deck.sub_decks
    if sub_decks:
        # Move all sub-decks to the parent deck
        for sub_deck in deck.sub_decks:
            sub_deck.parent_id = parent_deck.id # If the parent deck is None, it will be set to the root deck
    
    # Delete all cards in the deck
    for card in deck.cue_cards:
        db.session.delete(card)

    # Delete the deck itself
    db.session.delete(deck)
    db.session.commit()
    flash(f'Deck "{deck.name}" deleted successfully! Sub-decks have been moved to the parent deck.', "success")
    

    return redirect(url_for('views.decks'))





# ------- OLD CODE -------

# @views.route('/', methods=['GET', 'POST']) # This is a route decorator, it tells Flask what URL should trigger the function
# @login_required # This is a decorator from Flask-Login that requires the user to be logged in
# def home():
#     if request.method == 'POST':
#         note = request.form.get('note')

#         if len(note) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             new_note = Note(data=note, user_id=current_user.id)
#             db.session.add(new_note)
#             db.session.commit()
#             flash('Note added!', category='success')
    
#     return render_template("home.html", user=current_user)


# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({}) # You must return something, so we return an empty JSON object