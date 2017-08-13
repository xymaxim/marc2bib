"""Here are all currently defined tag-functions.

- common for all entry types:
    address, author, edition, editor, note, pages, publisher,
    series, title, volume, year
"""

def _get_subfield(record, subfield):
    try:
        f, subf = subfield[:3], subfield[-1:]
        rv = record[f][subf]
    except TypeError: 
        rv = None
    return rv

def common_address(record):
    field = record.get_fields('260', '264')[0]
    address = field['a']
    return address.replace('[', '').replace(']', '').rstrip(' : ')

def common_author(record):
    field = record['100']
    if field:
        return field['a'].rstrip('.')
    else:
        return None

def common_edition(record):
    field = record['250']
    if field:
        return field['a']
    else:
        return None

def common_editor(record):
    eds = [ed['a'].rstrip(',') for ed in record.get_fields('700')]
    return ' and '.join(eds)

def common_publisher(record):
    return record.publisher().rstrip(',').rstrip(' ;')

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

def common_year(record):
    return record.pubyear().lstrip('c').rstrip('.')

def common_volume(record):
    field = record['300']
    if field:
        return field['a']
    else:
        return None

def common_pages(record):
    raise NotImplementedError

def common_note(record):
    raise NotImplementedError

def common_series(record):
    field = record['490']
    if field:
        return field['a'].rstrip(',')
    else:
        return None

