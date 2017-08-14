"""Here are all currently defined tag-functions.

- common for all entry types:
    address, author, edition, editor, note, pages, publisher,
    series, title, volume, year

- techreport:
    institution
"""

default_req_tagfuncs = {}
default_opt_tagfuncs = {}

def req_tagfunc(bibtype, tag):
    def layer(func):
        def wrapper(*args):
            default_req_tagfuncs[bibtype] = tag
            func(*args)
        return wrapper
    return layer

def opt_tagfunc(bibtype, tag):
    def layer(func):
        def wrapper(*args):
            default_opt_tagfuncs[bibtype] = tag
            func(*args)
        return wrapper
    return layer


def _get_subfield(record, subfield):
    try:
        f, subf = subfield[:3], subfield[-1:]
        rv = record[f][subf]
    except TypeError: 
        rv = None
    return rv

@req_tagfunc('common', 'address')
def common_address(record):
    field = record.get_fields('260', '264')[0]
    address = field['a']
    return address.replace('[', '').replace(']', '').rstrip(' : ')

@req_tagfunc('common', 'author')
def common_author(record):
    field = record['100']
    if field:
        return field['a'].rstrip('.')
    else:
        return None

@req_tagfunc('common', 'edition')
def common_edition(record):
    field = record['250']
    if field:
        return field['a']
    else:
        return None

@opt_tagfunc('common', 'editor')
def common_editor(record):
    eds = [ed['a'].rstrip(',') for ed in record.get_fields('700')]
    return ' and '.join(eds)

@req_tagfunc('common', 'publisher')
def common_publisher(record):
    return record.publisher().rstrip(',').rstrip(' ;')

@req_tagfunc('common', 'title')
def common_title(record):
    title = record['245']['a']
    subtitle = record['245']['b']
    if subtitle:
        # Remove the extra whitespace between the title and a colon,
        # or append a colon to the title.
        # (Title : subtitle -> Title: subtitle)
        # (Title subtitle -> Title: subtitle)
        title = '{}: '.format(title.rsplit(' :')[0])
        rv = title + subtitle.rstrip('.')
    else:
        rv = title
    return rv.rstrip(' /')

@req_tagfunc('common', 'year')
def common_year(record):
    return record.pubyear().lstrip('c').rstrip('.')

@opt_tagfunc('common', 'volume')
def common_volume(record):
    field = record['300']
    if field:
        return field['a']
    else:
        return None

@opt_tagfunc('common', 'pages')
def common_pages(record):
    raise NotImplementedError

@opt_tagfunc('common', 'note')
def common_note(record):
    raise NotImplementedError

@opt_tagfunc('common', 'series')
def common_series(record):
    field = record['490']
    if field:
        return field['a'].rstrip(',')
    else:
        return None

    
@req_tagfunc('techreport', 'institution')
def techreport_institution(record):
    fields = record.get_fields('710')
    parts = []
    for f in fields:
        parts.append('{} {}'.format(f['a'], f['b']))
    return ' '.join(parts)
    
