#!/usr/bin/env python3
"""main.py -- entry point for the news-image-20261123 competition.

Copies the poster image held in this repository to the output directory
as entry.png. Pure Python 3.13 standard library, no network, deterministic:
the same bytes are written on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "poster.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
