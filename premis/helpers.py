import json
import logging
import premis.settings
import premis.version

logger = logging.getLogger('inventree')

def constructPathString(path, max_chars=250):
    """Construct a 'path string' for the given path.

    Arguments:
        path: A list of strings e.g. ['path', 'to', 'location']
        max_chars: Maximum number of characters
    """

    pathstring = '/'.join(path)

    idx = 0

    # Replace middle elements to limit the pathstring
    if len(pathstring) > max_chars:
        mid = len(path) // 2
        path_l = path[0:mid]
        path_r = path[mid:]

        # Ensure the pathstring length is limited
        while len(pathstring) > max_chars:

            # Remove an element from the list
            if idx % 2 == 0:
                path_l = path_l[:-1]
            else:
                path_r = path_r[1:]

            subpath = path_l + ['...'] + path_r

            pathstring = '/'.join(subpath)

            idx += 1

    return pathstring

def construct_absolute_url(*arg):
    """Construct (or attempt to construct) an absolute URL from a relative URL.

    This is useful when (for example) sending an email to a user with a link
    to something in the InvenTree web framework.

    This requires the BASE_URL configuration option to be set!
    """
    base = str(settings.get_setting('INVENTREE_BASE_URL'))

    url = '/'.join(arg)

    if not base:
        return url

    # Strip trailing slash from base url
    if base.endswith('/'):
        base = base[:-1]

    if url.startswith('/'):
        url = url[1:]

    url = f"{base}/{url}"

    return url

def str2bool(text, test=True):
    """Test if a string 'looks' like a boolean value.

    Args:
        text: Input text
        test (default = True): Set which boolean value to look for

    Returns:
        True if the text looks like the selected boolean value
    """
    if test:
        return str(text).lower() in ['1', 'y', 'yes', 't', 'true', 'ok', 'on', ]
    else:
        return str(text).lower() in ['0', 'n', 'no', 'none', 'f', 'false', 'off', ]

def is_bool(self):
        """Check if this setting is required to be a boolean value."""
        validator = self.__class__.get_setting_validator(self.key, **self.get_kwargs())

        return self.__class__.validator_is_bool(validator)

def MakeBarcode(object_name, object_pk, object_data=None, **kwargs):
    """Generate a string for a barcode. Adds some global InvenTree parameters.

    Args:
        object_type: string describing the object type e.g. 'StockItem'
        object_id: ID (Primary Key) of the object in the database
        object_url: url for JSON API detail view of the object
        data: Python dict object containing extra datawhich will be rendered to string (must only contain stringable values)

    Returns:
        json string of the supplied data plus some other data
    """
    if object_data is None:
        object_data = {}

    url = kwargs.get('url', False)
    brief = kwargs.get('brief', True)

    data = {}

    if url:
        request = object_data.get('request', None)
        item_url = object_data.get('item_url', None)
        absolute_url = None

        if request and item_url:
            absolute_url = request.build_absolute_uri(item_url)
            # Return URL (No JSON)
            return absolute_url

        if item_url:
            # Return URL (No JSON)
            return item_url
    elif brief:
        data[object_name] = object_pk
    else:
        data['tool'] = 'Premis'
        data['version'] = premis.version.premisVersion()
        data['instance'] = premis.version.premisInstanceName()

        # Ensure PK is included
        object_data['id'] = object_pk
        data[object_name] = object_data

    return json.dumps(data, sort_keys=True)