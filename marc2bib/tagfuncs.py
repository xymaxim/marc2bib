"""Here are all currently defined tag-functions."""

import re


def get_address(record):
    field = record.get_fields('260', '264')[0]
    address = field['a']
    return address.replace('[', '').replace(']', '').rstrip(' : ')

def get_author(record):
    field = record['100']
    if field:
        return field['a'].rstrip('.')
    else:
        return None

def get_edition(record):
    field = record['250']
    if field:
        return field['a']
    else:
        return None

def get_editor(record):
    eds = [ed['a'].rstrip(',') for ed in record.get_fields('700')]
    if eds:
        return ' and '.join(eds)
    else:
        return None

def get_publisher(record):
    publisher = record.publisher()
    if publisher:
        return publisher.rstrip(',').rstrip(' ;')
    else:
        return None

def get_title(record):
    field = record['245']
    
    try:
        title = field['a']
    except TypeError:
        return None
    try:  
        subtitle = field['b']
    except TypeError:
        subtitle = None
    
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

def get_year(record):
    year = record.pubyear()
    if year:
        return year.lstrip('c').rstrip('.')
    else:
        return None

def get_volume(record):
    field = record['300']
    if field:
        return field['a']
    else:
        return None

def get_pages(record):
    field = record['300']
    p = re.search('([0-9]+) p.', field['a'])

    if p:
        pages = p.group(1)
        return pages
    else:
        return None

def get_note(record):
    raise NotImplementedError

def get_series(record):
    field = record['490']
    if field:
        return field['a'].rstrip(',')
    else:
        return None

