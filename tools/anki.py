#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A collection of utilities for adding cards to Anki's DB."""
from itertools import chain
from typing import List

from bs4 import BeautifulSoup as BS

import anki

# Anki Schema: https://github.com/ankidroid/Anki-Android/wiki/Database-Structure

# Show models and decks
# c.models.all()
# c.decks.all()
# tag:200-wichtigsten-deutschen-Adjektive

# c.findCards('tag:xxx') -> List[Integer]
# c.getCard(id) -> anki.cards.Card
# c.getNote(anki.cards.Card.nid) -> anki.notes.Note


# I often put silent hyphens to my cards to improve their layout.
# This function cleans them out for printing inside a CLI.
def remove_silent_hyphens(input: str) -> str:
    return input.replace('\u00ad', '')


def get_related_double_notes(col: anki.collection._Collection, adj0: str,
                             adj1: str):
    """Finds language cards related to adjs.

    This function searches through my collection looking for flashcards for
    adjs. The two relevant card types are:

    * Image Occlusion cards with the both adjectives and a cloze box hiding
      them.
    * Cloze cards simulating what Image Occlusion cards do.
    """
    nids = []
    nids.extend(
        list(col.findNotes("tag:{} tag:{}".format(adj0, adj1))) +
        list(col.findNotes("{} {}".format(adj0, adj1))))
    nids = list(set(nids))
    notes = [col.getNote(nid) for nid in nids]
    image_occlusion_notes = []
    normal_notes = []
    for note in notes:
        model = note.model()
        if not model:
            raise Exception(
                "Found a note without a model. " +
                "Correct the assumption that every note has a model.")
        if model['name'] == "Image Occlusion Enhanced":
            image_occlusion_notes.append(note)
            continue

        normal_notes.append(note)

    return (image_occlusion_notes, normal_notes)


def get_related_notes(col: anki.collection._Collection, adjs: List[str]):
    """Finds language cards related to `adjs`.

    This function searches through my collection looking for flashcards for
    `adjs`. The two relevant card types are:

    * Image Occlusion cards with the both adjectives and a cloze box hiding
      them.
    * Simple front-only and front-and-back cards with a single adjective in the
      first field.
    """
    nids = []
    for adj in adjs:
        nids.extend(
            list(col.findNotes("tag:" + adj)) + list(col.findNotes(adj)))
    nids = list(set(nids))
    notes = [col.getNote(nid) for nid in nids]
    image_occlusion_notes = []
    normal_notes = []
    for note in notes:
        model = note.model()
        if not model:
            raise Exception(
                "Found a note without a model. " +
                "Correct the assumption that every note has a model.")
        if model['name'] == "Image Occlusion Enhanced":
            image_occlusion_notes.append(note)
            continue

        top_field = BS(note.fields[0]).text
        for adj in adjs:
            if top_field == adj:
                normal_notes.append(note)
                continue

        # Just to be sure, also add notes that contain an image from
        # deutschlernerblog.
        for f in note.fields:
            if f.find('Adjektive') != -1:
                normal_notes.append(note)
                continue

    return (image_occlusion_notes, normal_notes)


def open_my_collection() -> anki.collection._Collection:
    return anki.storage.Collection(
        '/home/grzesiek/Documents/Anki/grzesiek/collection.anki2')
