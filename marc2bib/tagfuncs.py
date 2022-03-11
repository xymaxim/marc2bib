"""Here are all currently defined tag-functions."""

import re


def get_address(record):
    # https://www.loc.gov/marc/bibliographic/bd25x28x.html
    fields = record.get_fields('260', '264')
    if fields:
        field = fields[0]
        return field['a'].replace('[', '').replace(']', '').rstrip(': ')
    else:
        return None

def get_author(record):
    # https://www.loc.gov/marc/bibliographic/bd1xx.html
    # https://www.loc.gov/marc/bibliographic/bd400.html
    # https://www.loc.gov/marc/bibliographic/bd600.html
    # https://www.loc.gov/marc/bibliographic/bd800.html
    fields = record.get_fields('100', '110', '400', '600', '800')
    if fields:
        field = fields[0]
        # In this case the subfield value is a pronoun
        if field.tag == '400' and field.indicator2 == '1':
            rv = None
        else:
            value = field['a']
            # Check if the subfield value ends with initials
            if re.findall(r'(?:[A-Z].)+$', value):
                rv = value.rstrip(',: ')
            else:
                rv = value.rstrip('.,: ')
            return rv
    else:
        return None

def get_edition(record):
    # https://www.loc.gov/marc/bibliographic/bd250.html
    field = record['250']
    if field:
        return field['a'].rstrip('/= ')
    else:
        return None

def get_editor(record):
    eds = [ed['a'].rstrip(',') for ed in record.get_fields('700')]
    if eds:
        return ' and '.join(eds)
    else:
        return None

def get_publisher(record):
    # https://www.loc.gov/marc/bibliographic/bd25x28x.html
    publisher = record.publisher()
    if publisher:
        return publisher.rstrip(',: ')
    else:
        return None

def get_title(record):
    # https://www.loc.gov/marc/bibliographic/bd245.html
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
    # https://www.loc.gov/marc/bibliographic/bd25x28x.html
    year = record.pubyear()
    if year:
        return year.lstrip('c').rstrip('.')
    else:
        return None

def get_volume(record):
    # https://www.loc.gov/marc/bibliographic/bd300.html
    field = record['300']
    if field:
        return field['a']
    else:
        return None

def get_pages(record):
    # https://www.loc.gov/marc/bibliographic/bd300.html
    field = record['300']
    if field:
        p = re.search('([0-9]+) p.', field['a'])
        return p.group(1) if p else None
    else:
        return None

def get_note(record):
    raise NotImplementedError

def get_series(record):
    # https://www.loc.gov/marc/bibliographic/bd490.html
    field = record['490']
    if field:
        return field['a'].rstrip(',')
    else:
        return None

