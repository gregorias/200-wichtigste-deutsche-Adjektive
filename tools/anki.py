#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A collection of utilities for adding cards to Anki's DB."""
import anki

# Anki Schema: https://github.com/ankidroid/Anki-Android/wiki/Database-Structure

# Show models and decks
# c.models.all()
# c.decks.all()
# tag:200-wichtigsten-deutschen-Adjektive

# c.findCards('tag:xxx') -> List[Integer]
# c.getCard(id) -> anki.cards.Card
# c.getNote(anki.cards.Card.nid) -> anki.notes.Note


def open_my_collection() -> anki.collection._Collection:
    return anki.storage.Collection(
        '/home/grzesiek/Documents/Anki/grzesiek/collection.anki2')
