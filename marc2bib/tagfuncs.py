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
    return ' and '.join(eds)

def get_publisher(record):
    return record.publisher().rstrip(',').rstrip(' ;')

def get_title(record):
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
        rv = title.rstrip(' /')
    return rv

def get_year(record):
    return record.pubyear().lstrip('c').rstrip('.')

def get_volume(record):
    field = record['300']
    if field:
        return field['a']
    else:
        return None
