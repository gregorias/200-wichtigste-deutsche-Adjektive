#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This gist uses tools to add 100 German cloze image cards."""
from contextlib import closing
from pathlib import PosixPath
import os
from typing import List

import anki

import tools.anki
from tools.process import DoubleAdjectivePic, SingleAdjectivePic

ANKI_DB = PosixPath('/home/grzesiek/Documents/Anki/grzesiek/collection.anki2')
assert (ANKI_DB.is_file())
IMAGE_DIR = PosixPath('images/').absolute()
assert (IMAGE_DIR.is_dir())
SHARED_TAGS = {'200-wichtigsten-deutschen-adjektive', 'Adjektiv'}
DOUBLE_CLOZE_TEMPLATE = """
<div style="display:flex;justify-content:center;">
  <div style="text-align:center;">
    <img src="{left_pic}" style="max-height:200px"/>
    <div>{{{{c1::{left_word}}}}}</div>
  </div>
  <div style="text-align:center;">
    <img src="{right_pic}" style="max-height:200px"/>
    <div>{right_cloze}</div>
  </div>
</div>
"""


def load_images() -> List[DoubleAdjectivePic]:
    pics = []
    import os
    for img in IMAGE_DIR.iterdir():
        pics.append(DoubleAdjectivePic.from_original(str(img)))
    return pics


def change_model_to_cloze(
        anki_collection: anki.collection._Collection) -> None:
    """Returns the id of the "cloze" model"""
    for m in anki_collection.models.all():
        if m['name'] == 'Cloze':
            anki_collection.models.setCurrent(m)
            return None
    assert (False)


def get_cloze_field(left_pic: str, left_adj: str, right_pic: str,
                    right_adj: str) -> str:
    if right_adj.startswith('un'):
        right_cloze = 'un{{c1::' + right_adj[2:] + '}}'
    elif right_adj.startswith('nicht '):
        right_cloze = 'nicht {{c1::' + right_adj[6:] + '}}'
    elif right_adj.endswith('los'):
        right_cloze = '{{c1::' + right_adj[:-3] + '}}los'
    else:
        right_cloze = '{{c2::' + right_adj + '}}'
    return DOUBLE_CLOZE_TEMPLATE.format(
        left_pic=left_pic,
        left_word=left_adj,
        right_pic=right_pic,
        right_cloze=right_cloze,
    )


def add_a_double_cloze_note(dap: DoubleAdjectivePic,
                            col: anki.collection._Collection):
    change_model_to_cloze(col)
    note = col.newNote(forDeck=False)
    note.model()['did'] = col.decks.id("200")  # type: ignore
    left_sap, right_sap = [sap.remove_subs() for sap in dap.split()]
    if left_sap.get_size()[1] > 400:
        left_sap, right_sap = (left_sap.resize(scale=0.5),
                               right_sap.resize(scale=0.5))
    left_pic = col.media.addFile(left_sap.get_filename())
    right_pic = col.media.addFile(right_sap.get_filename())
    note.fields[0] = get_cloze_field(left_pic, dap.left_adjective, right_pic,
                                     dap.right_adjective)
    note.tags = (list(SHARED_TAGS) +
                 [dap.left_adjective, dap.right_adjective] + ['double'])
    print("Adding an image for " +
          str((dap.left_adjective, dap.right_adjective)))
    col.addNote(note)
    note.flush()


def main(anki_collection: anki.collection._Collection):
    daps = load_images()
    for dap in daps:
        add_a_double_cloze_note(dap, col)
    col.save()


if __name__ == "__main__":
    with closing(anki.Collection(str(ANKI_DB))) as col:
        main(col)
