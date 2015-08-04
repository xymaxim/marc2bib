__all__ = ['convert']

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from pymarc import MARCReader


def get_title(record):
    value = record['245']['a']
    return value.rstrip(' /')

def get_author(record):
    value = record['245']['c']
    return value.rstrip('.')

def get_edition(record):
    return record['250']['a']

def get_year(record):
    val = record['260']['c']
    return val[1:-1]

DEFAULT_TAGFUNCS = {
    'title': get_title,
    'author': get_author,
    'edition': get_edition,
    'year': get_year,
}


def convert(record, bibtype, bibkey=None, tagfuncs=None):
    tagfuncs_ = DEFAULT_TAGFUNCS.copy()
    if tagfuncs:
        tagfuncs_.update(tagfuncs)

    if bibkey is None:
        surname = get_author(record).split(',')[0].split()[-1]
        bibkey = surname + get_year(record)

    entry = {'ENTRYTYPE': bibtype, 'ID': bibkey}
    for (tag, func) in tagfuncs_.items():
        entry[tag] = func(record)

    db = BibDatabase()
    db.entries.append(entry)
    return BibTexWriter().write(db)
