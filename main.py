#!/usr/bin/env python3
"""The World in One Day - entry program for make.fun's news-image-20261118.

The entry itself is the editorial poster ``news-2026-11-18.png`` in this
repository: one image that sums up the world news of 18 November 2026.
This program is the entry's deterministic runner. It verifies the poster
file (presence, PNG signature, integrity hash) and prints the day's five
stories as a fixed action log, identical on every run.

Standard library only. No network, no randomness, no clock.
"""

import hashlib
import struct
import sys
from pathlib import Path

COMPETITION = "news-image-20261118"
NEWS_DATE = "2026-11-18"
IMAGE_FILE = "news-2026-11-18.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# The five stories the poster sums up, in panel order (left to right).
STORIES = [
    (
        "Asia-Pacific",
        "Xi and Putin meet in Shenzhen ahead of a historic trilateral "
        "summit with Trump",
    ),
    (
        "Middle East",
        "US strikes Iran's Qeshm Island missile site; Iran answers with "
        "drones on Bahrain and Kuwait",
    ),
    (
        "Ukraine",
        "Ukraine hits the Kerch Bridge to Crimea for a second day and a "
        "road span collapses into the strait",
    ),
    (
        "United States",
        "Peltola wins Alaska and Democrats take a projected 56-44 Senate "
        "majority",
    ),
    (
        "Africa",
        "Ebola outbreak in DR Congo more than doubles, past 11,000 cases, "
        "children hit hardest",
    ),
]


def load_poster(path):
    """Read the poster and return its bytes, or raise ValueError."""
    if not path.is_file():
        raise ValueError("poster file is missing: %s" % path.name)
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("poster file is not a PNG: %s" % path.name)
    return data


def poster_dimensions(data):
    """Return the poster's (width, height) from its PNG IHDR chunk.

    The IHDR chunk always follows the 8-byte PNG signature: 4 bytes of
    chunk length, the 4-byte chunk name "IHDR", then width and height as
    big-endian 32-bit integers.
    """
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("poster PNG has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    poster_path = Path(__file__).resolve().parent / IMAGE_FILE
    try:
        poster = load_poster(poster_path)
        width, height = poster_dimensions(poster)
    except ValueError as problem:
        print("ERROR | %s" % problem)
        return 1

    digest = hashlib.sha256(poster).hexdigest()

    print("ENTRY | %s" % COMPETITION)
    print("DATE | %s" % NEWS_DATE)
    print("TITLE | The World in One Day")
    for number, (region, headline) in enumerate(STORIES, start=1):
        print("STORY %d | %s | %s" % (number, region, headline))
    print(
        "IMAGE | %s | %dx%d | bytes=%d | sha256=%s"
        % (IMAGE_FILE, width, height, len(poster), digest)
    )
    print("STATUS | ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
