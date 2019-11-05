class FantasyApiException(Exception):
    """The Fantasy API Exception Class.

    Args:
        error (str): Human readable string describing the exception.

    Attributes:
        error (str): Human readable string describing the exception.

    """
    def __init__(self, error):
        self.error = error

    def get_message(self):
        """Function used to get exception output.

        Returns:
            obj: The JSON output message for the exception.

        """
        return {'error': self.error}

    def __str__(self):
        return self.error


class FantasyConnectionException(FantasyApiException):
    pass


class FantasyDataException(FantasyApiException):
    pass


class LocalDataNotFoundException(FantasyApiException):
    pass


class ValidationException(FantasyApiException):
    pass
