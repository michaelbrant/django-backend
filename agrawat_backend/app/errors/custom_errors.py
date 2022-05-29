class Error(Exception):
    def __init__(self, value=""):
        if not hasattr(self, "value"):
            self.value = value

    def __str__(self):
        return repr(self.value)


###############
# User Errors #
###############


class CustomError(Error):
    message = "This is an example of a custom error"
    internal_error_code = 40101
