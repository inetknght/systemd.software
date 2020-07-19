#!/usr/bin/env python3

import sys
from os import makedirs
from pathlib import Path
from html import escape
from shutil import copytree
from shutil import copy2

from markdown import markdown as do_markdown
from bs4 import BeautifulSoup

markdown = Path("markdown")
examples = Path("examples")
templates = Path("templates")
www = Path("www")

t = templates / "readme.html"

readme_md = Path("README.md")
examples_md = markdown / examples / "examples.md"

build = {
    (readme_md,     t, www / "index.html"),
    (examples_md,   t, www / examples / "index.html"),
}

def blap_dir(d):
    target = (www / d.relative_to(markdown))
    makedirs(target, exist_ok=True)
    for f in d.iterdir():
        if not f.is_file():
            continue
        if "README.md" == f.name:
            continue
        copy2(f, target)

def subdirify(current_md, body):
    for link in body.find_all("a"):
        href = link.get("href")
        #
        # No link? wtf markdown broke
        if None == href:
            # wat
            print("wat")
            continue
        #
        # Not a plain dirname? Escape hatch.
        if "/" in href:
            continue
        p = link.parent
        #
        # Not a list item? Escape hatch.
        if "li" != p.name:
            print("noli: {}".format(p))
            continue
        #
        # Not a directory? No files to list.
        d = (current_md.parent / href)
        if not d.is_dir():
            print("not dir: {}".format(d))
            continue
        #
        # Build a new list
        l = BeautifulSoup("".join(
            "<li><a href=\"{}\"><code>{}</code></a></li>".format(
                f.relative_to(current_md.parent),
                escape(f.name)
            )
            for f in d.iterdir()
            if f.is_file()
            #
            # Don't add the README.md for the directory
            if f.name != "README.md"
        ), "html5lib")
        #
        # Work the stuffs.
        blap_dir(d)
        #
        # Replacement!
        p.replaceWith(l)

def do_build(md_in, t_in, path_out):
    with open(md_in, "r") as f:
        md = f.read()
    with open(t_in, "r") as f:
        t_html = BeautifulSoup(f, "html5lib")
    content = BeautifulSoup(do_markdown(md), "html5lib")
    subdirify(md_in, content.body)
    t_html.body.replaceWith(content.body)
    with open(path_out, "w") as f:
        f.write(str(t_html))

for md_in, t_in, path_out in build:
    do_build(md_in, t_in, path_out)
