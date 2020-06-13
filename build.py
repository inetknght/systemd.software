
import sys

from markdown import markdown
from bs4 import BeautifulSoup

with open("README.md", "r") as f:
    readme_md = f.read()
with open("templates/readme.html", "r") as f:
    index_html = BeautifulSoup(f, "html5lib")

content = BeautifulSoup(markdown(readme_md), "html5lib")
index_html.body.replaceWith(content.body)

with open("www/index.html", "w") as f:
    f.write(str(index_html))
