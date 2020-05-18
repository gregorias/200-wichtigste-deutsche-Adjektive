# 200 wichtigsten deutschen Adjektive

A collection of tools for downloading and processing adjective-pictures from
deutschlernerblog.de.

## Overview

This repo contains one executable package `tools.scrape` that downloads images
from deutschlernerblog.de

## Background

I use [Anki](https://apps.ankiweb.net/) flashcards to learn languages. I noticed
that deutschlernerblog.de has a collection of 100 images representing
adjectives, and I thought that they would make for good flashcards: the images
look good and placing opposite words side-by-side makes it easy to create a
clear flashcard.

## For Developers

### Development shell

For development comfort, this project  uses Pipenv to manage dependencies and
the dev environment. Before each dev session run

    psh

to activate a dev subshell. The subshell configures shell and python
environments for this project.

### Unit testing

Run

    testall

to run this project's static type checker and unit tests.
