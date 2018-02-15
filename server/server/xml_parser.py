import logging
import xml.etree.ElementTree as eT

DEFAULT_SQUASH_ELEMENTS = [
    'component',
    'files',
    'value',
    'FileTracker'
]

log = logging.getLogger(__name__)


def parse(filename):
    log.debug('Parsing XML file: %s', filename)
    return __parse(eT.parse(filename).getroot())


def __parse(element, squash=None):
    data = {}

    if squash is None:
        squash = DEFAULT_SQUASH_ELEMENTS

    for child in element:
        if 'value' in child.attrib:
            data[child.attrib['name']] = child.attrib['value']
        elif child.find('list') is not None:
            list_data = []

            for e in child.find('list'):
                list_data.append(__parse(e))

            data[child.attrib['name']] = list_data
        elif child.find('map') is not None:
            squash_child = child.attrib['name'] in squash
            map_data = data if squash_child else {}

            for entry in child.find('map'):
                map_data[entry.attrib['key']] = __parse(entry)

            if not squash_child:
                data[child.attrib['name']] = map_data
        elif child.tag in squash:
            data = __parse(child)
        else:
            data[child.tag] = __parse(child) if len(
                child) > 0 else child.text or ''

    return data
