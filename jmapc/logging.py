import logging

# Set default logging handler to avoid "No handler found" warnings.
log = logging.getLogger(__package__)
log.addHandler(logging.NullHandler())
