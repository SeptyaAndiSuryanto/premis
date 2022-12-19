import sys


def isImportingData():
    """Returns True if the database is currently importing data, e.g. 'loaddata' command is performed."""
    return 'loaddata' in sys.argv