"""This is a main marc2bib package file.

Make sure to check out the FAQ [1] for the MARC 21 at the Library of
Congress (LOC) website. There is a lot information located on the main
page [2] -- but first, take a look at a brief description and a summary
of the MARC 21 fields [3]. While hacking on this package, you may also
find useful both the full and concise versions of the "MARC 21 Format
for Bibliographic Data" document [4]. Information regarding the BibTeX
entry types and corresponding fields can be found in Section 3 of the
original manual dated 1988 [5].

[1] http://www.loc.gov/marc/faq.html
[2] http://www.loc.gov/marc/
[3] http://www.loc.gov/marc/umb/
[4] http://www.loc.gov/marc/bibliographic/
[5] http://ctan.uni-altai.ru/biblio/bibtex/base/btxdoc.pdf
"""

__all__ = ['convert']

from pymarc import MARCReader


def get_author(record):
    val = record['245']['c']
    return val.rstrip('.')

def get_edition(record):
    return record['250']['a']

def get_publisher(record):
    val = record['260']['b']
    return val.strip(',')

def get_title(record):
    val = record['245']['a']
    return val.rstrip('/')

def get_year(record):
    # FIXME
    val = record['260']['c']
    return val[1:-1]

BOOK_TAGFUNCS = {
    'author': get_author,
    'edition': get_edition,
    'publisher': get_publisher,
    'title': get_title,
    'year': get_year,
}


def _as_bibtex(bibtype, bibkey, fields):
    bibtex = '@{0}{{{1}'.format(bibtype, bibkey)
    for tag, value in sorted(fields.items()):
        bibtex += ',\n {0} = {{{1}}}'.format(tag, value)
    bibtex += '\n}\n'
    return bibtex

def convert(record, bibtype='book', bibkey=None, tagfuncs=None):
    tagfuncs_ = BOOK_TAGFUNCS.copy()
    if tagfuncs:
        tagfuncs_.update(tagfuncs)

    if bibkey is None:
        surname = get_author(record).split(',')[0].split()[-1]
        bibkey = surname + get_year(record)

    fields = {}
    for tag, func in tagfuncs_.items():
        value = func(record)
        if not isinstance(value, str):
            msg = ("Return value from {} for {} tag "
                   "should be a string").format(func, tag)
            raise TypeError(msg)
        fields[tag] = func(record)

    return _as_bibtex(bibtype, bibkey, fields)
