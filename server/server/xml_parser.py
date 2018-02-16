import logging
import xml.etree.ElementTree as eT

# Elements to squash
# Squashing an element will include its children but not itself
DEFAULT_SQUASH_ELEMENTS = [
    'component',
    'files',
    'value',
    'FileTracker'
]

log = logging.getLogger(__name__)


def parse(filename):
    """
    Parse an XML file given its path
    :param filename: The filename of the XML file
    :return: The parsed XML data
    """
    log.debug('Parsing XML file: %s', filename)
    return __parse(eT.parse(filename).getroot())


def __parse(element, squash=None):
    """
    Parse an XML element into a dict
    :param element: The element to parse
    :param squash: A list of element tags or attribute names to squash
    :return: The parsed element as a dict
    """
    data = {}

    if squash is None:
        squash = DEFAULT_SQUASH_ELEMENTS

    for child in element:
        if 'value' in child.attrib:
            # Add element name=value pair
            data[child.attrib['name']] = child.attrib['value']
        elif child.find('list') is not None:
            # Element contains a list child so store it as a list
            list_data = []

            for e in child.find('list'):
                list_data.append(__parse(e))

            data[child.attrib['name']] = list_data
        elif child.find('map') is not None:
            # Element contains a map child so store it as a dict
            squash_child = child.attrib['name'] in squash
            # Squash map if necessary
            map_data = data if squash_child else {}

            for entry in child.find('map'):
                map_data[entry.attrib['key']] = __parse(entry)

            if not squash_child:
                data[child.attrib['name']] = map_data
        elif child.tag in squash:
            # Element should be squash, so parse its child instead
            data = __parse(child)
        else:
            # Default parsing of element
            data[child.tag] = __parse(child) if len(
                child) > 0 else child.text or ''

    return data
