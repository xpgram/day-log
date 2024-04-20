
class LogstreamReadError(Exception):
    "Could not parse data from save."

class LogstreamInputError(Exception):
    "Could not parse data from input."

class LogstreamSaveError(Exception):
    "Could not serialize logstream object to save data."

class LogstreamRenderError(Exception):
    "Could not render logstream object for dislay."
