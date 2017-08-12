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

from functools import reduce

from pymarc import MARCReader, Record

from . import tagfuncs as book_tagfuncs


BOOK_REQ_TAGFUNCS = {
    'author': book_tagfuncs.common_author,
    'publisher': book_tagfuncs.common_publisher,
    'title': book_tagfuncs.common_title,
    'year': book_tagfuncs.common_year,
}

BOOK_OPT_TAGFUNCS = {
    'address': book_tagfuncs.common_address,
    'edition': book_tagfuncs.common_edition,
    'volume': book_tagfuncs.common_volume,
    'isbn': Record.isbn,
}


def _as_bibtex(bibtype, bibkey, fields, indent, align=False):
    tag_width = max(map(len, fields)) if align else 0
        
    bibtex = '@{0}{{{1}'.format(bibtype, bibkey)
    for tag, value in sorted(fields.items()):
        bibtex += ',\n{0}{1:<{width}} = {{{2}}}'.format(
            ' ' * indent, tag, value, width=tag_width)
    bibtex += '\n}\n'
    
    return bibtex

def convert(record, bibtype='book', bibkey=None, tagfuncs=None, **kw):
    """Converts an instance of :class:`pymarc.Record` to a BibTeX entry.

    By default all defined fields (tags) for the given `bibtype` are
    returned. For the book entry see keys in `BOOK_REQ_TAGFUNCS` and
    `BOOK_OPT_TAGFUNCS`. Use ``tagfuncs`` argument to extend or
    override returned tags. If you want to control the returned tags,
    use ``include`` argument instead.

    Args:
        record: An instance of :class:`pymarc.Record`.
        bibtype (Optional[str]): A BibTeX entry type. Currently only
            book entries are fully supported.
        bibkey (Optional[str]): A BibTeX citation key. If ``None``, then
            the author-date style is used, e.g. "hargittai2007". If the
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

    Returns:
        A BibTeX-formatted string.
    """
    ctx_tagfuncs = BOOK_REQ_TAGFUNCS.copy()

    include_arg = kw.get('include', 'required')
    if include_arg == 'all':
        ctx_tagfuncs.update(BOOK_OPT_TAGFUNCS)
    elif include_arg != 'required':
        # Check if include argument is iterable and not a string.
        # We are no longer interested in a string because all
        # possible values are already passed.
        try:
            assert not isinstance(include_arg, str)
            iter(include_arg)
        except (AssertionError, TypeError) as e:
            msg = ("include should be an iterable or one of "
                   "('required', 'all'), got {}".format(include_arg))
            e.args += (msg,)
            # XXX ValueError or something like that, actually.
            raise
        else:
            req_tags = list(BOOK_REQ_TAGFUNCS.keys())
            opt_tags = list(BOOK_OPT_TAGFUNCS.keys())
            if not set(include_arg).issubset(req_tags + opt_tags):
                raise ValueError("include contains unknown tag(s)")

            tagsfuncs_to_include = {tag: BOOK_OPT_TAGFUNCS[tag]
                                    for tag in include_arg}
            ctx_tagfuncs.update(tagsfuncs_to_include)

    if tagfuncs:
        ctx_tagfuncs.update(tagfuncs)

    fields = {}
    for tag, func in ctx_tagfuncs.items():
        field_value = func(record)
        if not isinstance(field_value, str) and field_value is not None:
            msg = ("Returned value from {} for {} tag "
                   "should be a string or None").format(func, tag)
            raise TypeError(msg)
        fields[tag] = field_value

    if fields['author'] == '':
        fields.pop('author')
        try:
            fields['editor'] = ctx_tagfuncs['editor'](record)
        except KeyError:
            fields['editor'] = book_tagfuncs.common_editor(record)

    if bibkey is None:
        try:
            authors_or_editors = fields['author']
        except KeyError:
            authors_or_editors = fields['editor']
        surname = authors_or_editors.split(',')[0]
        bibkey = surname.lower() + book_tagfuncs.common_year(record)

    indent = kw.get('indent', 1)
    align = kw.get('align', False)
    
    return _as_bibtex(bibtype, bibkey, fields, indent, align=align)
