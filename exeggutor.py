"""Builds exeggutor
"""
import sys
from io import BytesIO

import numpy as np
import praw
import requests
from PIL import Image

reddit = praw.Reddit('TuttleStripes')


def array_from_url(url: str) -> np.array:
    """Builds a numpy array from the content of an image url"""
    res = requests.get(url)
    with BytesIO(res.content) as bio:
        img = Image.open(bio)
        img.load()
    return np.array(img, np.uint8)


def build_exeggutor(subsort: str, limit=25) -> Image:
    sub = reddit.subreddit('upvoteexeggutor')
    nek = eval(f'sub.{subsort}(limit={limit})')
    arr = np.vstack([array_from_url(post.thumbnail) for post in nek])
    if subsort in ['new', 'controversial']:
        head = array_from_url(next(sub.top()).thumbnail)
        arr = np.vstack([head, arr])
    return Image.fromarray(arr)


if __name__ == "__main__":
    PIC = build_exeggutor(sys.argv[1], sys.argv[2])
    PIC.show()
    if len(sys.argv) == 4:
        PIC.save(f'{sys.argv[3]}')
