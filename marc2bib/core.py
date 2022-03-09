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

import warnings

from pymarc import MARCReader, Record

from . import tagfuncs as default_tagfuncs


# By default, book entry may contain either one of author or editor
# fields. See convert function to know how they are treated,
# especially in case if both fields are requested.
BOOK_REQ_TAGFUNCS = {
    'author': default_tagfuncs.get_author,
    'editor': default_tagfuncs.get_editor,
    'publisher': default_tagfuncs.get_publisher,
    'title': default_tagfuncs.get_title,
    'year': default_tagfuncs.get_year,
}

BOOK_OPT_TAGFUNCS = {
    'address': default_tagfuncs.get_address,
    'edition': default_tagfuncs.get_edition,
    'volume': default_tagfuncs.get_volume,
    'note': default_tagfuncs.get_note,
    'number': default_tagfuncs.get_volume,
    'pages': default_tagfuncs.get_pages,
    'series': default_tagfuncs.get_series,
    'isbn': Record.isbn,
}


class Marc2bibError(Exception):
    pass


def _isblank(string):
    return string.strip() == ''

def _as_bibtex(bibtype, bibkey, tags, indent, align):
    tag_width = max(map(len, tags)) if align else 0
        
    bibtex = f'@{bibtype}{{{bibkey}'
    for tag, value in sorted(tags.items()):
        bibtex += f',\n{" " * indent}{tag:<{tag_width}} = {{{value}}}'
    bibtex += '\n}\n'
    
    return bibtex


def map_tags(record, tagfuncs=None, **kw):
    ctx_tagfuncs = BOOK_REQ_TAGFUNCS.copy()
    include_arg = kw.get('include', 'required')

    if include_arg == 'all':
        ctx_tagfuncs.update(BOOK_OPT_TAGFUNCS)
    elif include_arg != 'required':
        # Check if `include_arg` argument is iterable and not a string.
        # We are no longer interested in a string because all
        # possible values are already passed.
        try:
            assert not isinstance(include_arg, str)
            iter(include_arg)
        except (AssertionError, TypeError) as e:
            msg = ("include_arg should be an iterable or one of "
                   f"('required', 'all'), got {include_arg}")
            e.args += (msg,)
            raise ValueError(e)
        else:
            # Ensure that all of the user-provided tags has a
            # tag-function defined by default in optional tags.
            if not all(tag in BOOK_OPT_TAGFUNCS for tag in include_arg):
                raise ValueError("include_arg contains unknown optional tag(s)")
            for tag in include_arg:
                ctx_tagfuncs[tag] = BOOK_OPT_TAGFUNCS[tag]

    if tagfuncs:
        ctx_tagfuncs.update(tagfuncs)

    tags = {}

    # Check for author field first, then editor.
    author = ctx_tagfuncs['author'](record)
    if author:
        # Editor field can be requested along with author.
        if 'editor' not in include_arg or 'editor' not in tagfuncs:
            ctx_tagfuncs.pop('editor')
    else:
        editor = ctx_tagfuncs['editor'](record)
        if editor is None:
            msg = "both author and editor (required) tags are treated empty."
            raise Marc2bibError(msg)
        else:
            ctx_tagfuncs.pop('author')
        
    for tag, func in ctx_tagfuncs.items():
        tag_value = func(record)
        if not isinstance(tag_value, str) and tag_value is not None:
            msg = (f"Returned value from {func} for {tag} tag "
                   "should be a string or None")
            raise TypeError(msg)

        if tag_value is None:
            msg = (f"The content of tag `{tag}` is None, "
                   "replacing it with an empty value")
            warnings.warn(UserWarning(msg))
            tag_value = ''

        allow_blank = kw.get('allow_blank', False)
        blank_and_allowed = _isblank(tag_value) and allow_blank
        if tag_value.strip() or blank_and_allowed:
            # Here we only accept non-blank field values, empty values
            # (if they are allowed by the given keyword argument), and also
            # all required tags.
            tags[tag] = tag_value

    return tags

def tags_to_bibtex(tags, bibtype='book', bibkey=None, indent=1, align=False):
    if bibkey is None:
        try:
            authors_or_editors = tags['author']
        except KeyError:
            authors_or_editors = tags['editor']
        surname = authors_or_editors.split(',')[0]
        bibkey_value = surname.lower() + tags['year']
    elif callable(bibkey):
        bibkey_value = bibkey(tags)
    else:
        bibkey_value = bibkey

    bibtex = _as_bibtex(bibtype, bibkey_value, tags, indent, align)

    return bibtex
    
def convert(record=None, ctx=None, bibtype='book', bibkey=None, tagfuncs=None, **kw):
    """Converts an instance of :class:`pymarc.Record` to a BibTeX entry.

    By default all defined (required and optional) fields (tags) for
    book entry are returned. Use ``tagfuncs`` argument to extend or
    override returned tags. If you want to control the returned tags,
    use ``include`` argument instead.

    Args:
        record: An instance of :class:`pymarc.Record`.
        bibtype (Optional[str]): A BibTeX entry type. Currently only
            book entries are fully supported.
        bibkey (Optional[str]): A BibTeX citation key. If ``None``, then
            the author-date style is used, e.g. "author2022". If the
            author is not provided, then the first editor will be used.
        tagfuncs (Optional[dict]): A dictionary with functions used to
            retrieve a BibTeX tag content. The key of the dictionary
            is the name of a particular tag. Your function (we call
            this tag-function) must take one argument, a reference to
            the given record, and return a string. Example usage::

            def tagfunc(record):
                # Insert your way to get the field value here.
                ...
            convert(record, tagfuncs={'tag': tagfunc})

    Keyword args:
        include: Defaults to 'all'. The value can be either
            * 'all' -- include all defined tags for the given ``bibtype``
            * 'required' -- include only required tags for the given
                            ``bibtype``
            * a list of tags to include together with the required
              ones. For example, ['edition'].
        indent (int): The tag line indentation. Defaults to 1.
        align (bool): If True, align tag values by the longest tag.
            Defaults to False.
        allow_blank (bool): If True, also include tags with a blank 
            content (empty or contains only whitespace characters)
            to the output. Defaults to False. 

    Returns:
        A BibTeX-formatted string.

    """
    indent = kw.get('indent', 1)
    align = kw.get('align', False)

    tags = map_tags(record, tagfuncs, **kw)
    bibtex = tags_to_bibtex(tags, bibtype, bibkey, indent, align)

    return bibtex
