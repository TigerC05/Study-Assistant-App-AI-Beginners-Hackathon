from flask import url_for

def display_deck_heirarchy_html(decks, level=0, deck_id=None):
    """
    Recursively generates HTML for displaying deck hierarchy.
    Example:
    <div class="list-group">
        <div class="list-group-item">
            <button class="btn btn-link text-decoration-none" data-bs-toggle="collapse" data-bs-target="#deck-1">
                <i class="bi bi-caret-right-fill toggle-arrow"></i>
            </button>
            <a href="/decks/1" class="text-dark text-decoration-none fw-bold">Deck 1</a>
        </div>
        <div class="collapse" id="deck-1">
            <!-- Sub-decks go here -->
        </div>
    </div>
    Args:
        decks (list): List of Deck objects.
        level (int): Current level in the hierarchy.
        deck_id (int): ID of the current deck.
    Returns:
        str: HTML string representing the deck hierarchy.
    """
    if level == 0: # At the top level, we need to create a div for the list group
        html = '<div class="list-group">' 
    else: # At a sub-level, we need to create a div for the collapse
        html = f'<div class="collapse" id="deck-{ deck_id }"  style="margin-left: {1.5*level}rem";>'
    for deck in decks:
        if deck.parent_id and level == 0: # If the deck has a parent and we are at the top level, we need to skip it
            continue
        # Create a div for each deck
        html += '<div class="list-group-item">'
        if deck.sub_decks: # If the deck has sub-decks, we need to create a button to toggle the collapse
            html += f'<button class="btn btn-link text-decoration-none" data-bs-toggle="collapse" data-bs-target="#deck-{ deck.id }">'
            html +=       '<i class="fa-solid fa-caret-right toggle-arrow"></i>'
            html +=  '</button>'
        else: # If the deck has no sub-decks, we need to create a span to add some space
            html += '<span class="ms-4"></span>'
        
        html += f'<a href="{url_for("views.overview_deck", deck_id=deck.id)}" class=" text-dark text-decoration-none fw-bold">{ htmlEscape(deck.name) }</a>'
        html += '</div>' # Close the list group item div

        # Recursively call the function to get sub-decks
        if deck.sub_decks:
            # print("DEBUG: Name: ", deck.name, ", ID: ", deck.id, ", Subdecks: ",deck.sub_decks)
            html += display_deck_heirarchy_html(deck.sub_decks, level + 1, deck.id)

    html += '</div>' # Close the collapse div
    if level == 0: # Close the list group div if we are at the top level
        html += '</div>'
    return html

def display_deck_list_html(decks, level=0, parent_deck_name=None):
    """
    Recursively generates HTML for displaying deck list.
    Args:
        decks (list): List of Deck objects.
        level (int): Current level in the hierarchy.
    Returns:
        str: HTML string representing the deck list.
    Example:
    <label for="parentDeck" class="form-label">Nest Under:</label>
    <select class="form-select" id="parentDeck" name="parent_deck">
        <option value="">None (Top-Level Deck)</option>
        <option value="1">My First Deck</option>
        <option value="6">My First Deck/My First Sub Deck</option>
        <option value="8">My First Deck/My First Sub Deck/My Sub Sub Deck</option>
        <option value="7">My First Deck/My Second Sub Deck</option>
        <option value="2">My Second Deck</option>
        ...
    </select>
    """
    if level == 0:
        html = '<label for="parentDeck" class="form-label">Nest Under:</label>'
        html += '<select class="form-select" id="parentDeck" name="parent_deck">'
        html += '<option value="">None (Top-Level Deck)</option>'
    else:
        html = ''
    for deck in decks:
        if deck.parent_id and level == 0:
            continue # Skip if the deck has a parent and we are at the top level
        else:
            if parent_deck_name:
                html += f'<option value="{ deck.id }">{ htmlEscape(parent_deck_name + "/" + deck.name) }</option>'
            else:
                html += f'<option value="{ deck.id }">{ htmlEscape(deck.name) }</option>'
        # Recursively call the function to get sub-decks
        if deck.sub_decks:
            if parent_deck_name:
                html += display_deck_list_html(deck.sub_decks, level + 1, htmlEscape(parent_deck_name + "/" + deck.name))
            else:
                html +=  display_deck_list_html(deck.sub_decks, level + 1, htmlEscape(deck.name))
    if level == 0:
        html += '</select>'
    return html
            

def htmlEscape(text):
    """
    Escapes HTML special characters in a string.
    Args:
        text (str): Input string.
    Returns:
        str: Escaped string.
    """
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;").replace("/", "&#x2F;")
