import common.models

PREMIS_VERSION = "0.1.0 dev"

def premisInstanceName():
    """Returns the InstanceName settings for the current database."""
    return common.models.PremisSetting.get_setting("PREMIS_INSTANCE", "")

def premisVersion():
    """Returns the InvenTree version string."""
    return PREMIS_VERSION.lower().strip()

