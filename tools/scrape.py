#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""An executable package that scrapes adjective images from deutschlernerblog.

This binary scrapes adjective images from deutschlernenblog and saves them to
images/ folder.
"""
import logging
import re
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup


def extract_filename_from_image_url(url: str) -> str:
    """
    >>> extract_filename_from_image_url('https://deutschlernerblog.de/wp-content/uploads/2017/07/wild_zahm_Adjektive_Deutsch_deutschlernerblog.png')
    'wild_zahm_Adjektive_Deutsch_deutschlernerblog.png'
    """
    filename_match = re.compile(r'([^/]+)$').search(url)
    if not filename_match:
        raise Exception("Could not find the filename in " + url)
    return filename_match[1]


def scrape_images_and_metadata_from_site(url: str) -> Tuple:
    logging.info('Scraping image sources from: ' + url)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text)

    imgs = soup.findAll('img')
    imgs = [
        img for img in imgs if img.has_attr('width') and img['width'] == '640'
        and img.has_attr('height') and img['height'] == '402'
        and not img.has_attr('data-lazy-src')
    ]
    srcs = [img['src'] for img in imgs]

    weiter = soup.find(string=re.compile('weiter\s+$'))
    next_link = weiter.next['href'] if weiter else None

    return (srcs, next_link)


def download_image(url: str) -> bytes:
    logging.info('Downloading image: ' + extract_filename_from_image_url(url))
    image = requests.get(url)
    image.raise_for_status()
    return image.content


def fetch_image_sources() -> List:
    WEBSITE_PART_1_URL = "https://deutschlernerblog.de/die-200-wichtigsten-deutschen-adjektive-mit-bildern-lernen-teil-1/"
    url = WEBSITE_PART_1_URL
    all_srcs = []
    while True:
        srcs, next_link = scrape_images_and_metadata_from_site(url)
        all_srcs.extend(srcs)
        if not next_link:
            break
        url = next_link
    return all_srcs


def main():
    logging.basicConfig(filename='scrape.log', level=logging.INFO)
    image_srcs = fetch_image_sources()
    metadata = []
    for img_url in image_srcs:
        fn = extract_filename_from_image_url(img_url)
        with open('images/' + fn, 'wb') as f:
            f.write(download_image(img_url))


if __name__ == "__main__":
    main()
