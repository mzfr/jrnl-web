import re

import markdown as markdown_lib
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

URL_RE = re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|'
                       r'(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:/[\+~%/\.\w\-_]*)?\??'
                       r'(?:[\-\+=&;%@\.\w_]*)#?(?:[\.!/\\\w]*))?)')


class URLify(Preprocessor):
    def run(self, lines):
        return [URL_RE.sub(r'<\1>', line) for line in lines]


class URLifyExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('urlify', URLify(md), '_end')


def markdown(text):
    """Processes GFM then converts it to HTML."""
    extensions = [URLifyExtension(), 'markdown.extensions.nl2br']

    text = markdown_lib.markdown(text, extensions)
    return text
